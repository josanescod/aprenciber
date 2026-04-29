from datetime import datetime, timezone, timedelta
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_auth_user
from app.dependencies.db import get_db
from app.infrastructure.docker.docker_client import get_docker_client
from app.infrastructure.docker.lab_provisioner import LabProvisioner
from app.infrastructure.scenarios.scenario_loader import load_scenario
from app.models.lab_instance import LabInstance
from app.repositories.lab_instance_repository import LabInstanceRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.schemas.lab import LabStartRequest, LabStartResponse, LabOut
from app.services.auth_provider import AuthenticatedUser
from app.infrastructure.ttyd.ttyd_manager import TtydManager
from app.services import ttyd_process_registry
from app.services.flag_service import generate_flag
from app.models.submission import Submission
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.user_progress_repository import UserProgressRepository
from app.schemas.submission import FlagSubmitRequest, FlagSubmitResponse


router = APIRouter(prefix="/api/labs", tags=["labs"])


@router.post(
    "/start", response_model=LabStartResponse, status_code=status.HTTP_201_CREATED
)
def start_lab(
    payload: LabStartRequest,
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    scenario_repo = ScenarioRepository(db)
    scenario = scenario_repo.get_by_slug(payload.scenario_slug)
    if scenario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found"
        )

    lab_repo = LabInstanceRepository(db)
    existing_labs = lab_repo.get_active_by_user(auth_user.id)

    if existing_labs:
        existing = existing_labs[0]

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Ja tens un laboratori actiu",
                "lab_id": existing.id,
            },
        )

    scenario_yaml_path = Path(scenario.yaml_path)
    if not scenario_yaml_path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scenario YAML not found: {scenario.yaml_path}",
        )

    try:
        scenario_data = load_scenario(scenario_yaml_path)
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading scenario: {exc}",
        ) from exc

    docker_client = get_docker_client()
    provisioner = LabProvisioner(docker_client)

    try:
        lab_data = provisioner.start_lab(scenario_data)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    # Generar el flag just després de provisionar el lab
    flag = generate_flag()

    lab = LabInstance(
        user_id=auth_user.id,
        scenario_id=scenario.id,
        status=lab_data["status"],
        containers_info=lab_data["containers_info"],
        networks_info=lab_data["networks_info"],
        flag_value=flag,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    )

    saved_lab = lab_repo.create(lab)

    # Injectar flag al contenidor target
    if scenario_data.flag is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Scenario flag configuration not found",
        )
    try:
        provisioner.inject_flag(
            containers_info=lab_data["containers_info"],
            flag_value=flag,
            flag_path=scenario_data.flag.path,
        )
        print(f"[flag] Injected into lab {saved_lab.id}")

    except (RuntimeError, OSError) as exc:
        print(f"[flag] Warning: could not inject flag into lab {saved_lab.id}: {exc}")

    # Iniciar ttyd per al contenidor atacant
    attacker_name = lab_data["containers_info"].get("attacker", {}).get("name")
    if attacker_name:
        ttyd_manager = TtydManager()
        try:
            port, pid = ttyd_manager.start_terminal(attacker_name)
            saved_lab.terminal_url = f"http://localhost:{port}"
            saved_lab.terminal_pid = pid
            lab_repo.update(saved_lab)
            ttyd_process_registry.register(saved_lab.id, pid)
            print(f"[ttyd] Started for lab {saved_lab.id} on port {port} (pid {pid})")
        except (OSError, ValueError) as exc:
            print(
                f"[ttyd] Warning: could not start terminal for lab {saved_lab.id}: {exc}"
            )

    return saved_lab


@router.get("/me/active", response_model=list[LabOut])
def get_my_active_labs(
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    lab_repo = LabInstanceRepository(db)
    return lab_repo.get_active_by_user(auth_user.id)


@router.get("/{lab_id}", response_model=LabOut)
def get_lab(
    lab_id: int,
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    lab_repo = LabInstanceRepository(db)
    lab = lab_repo.get_by_id(lab_id)

    if lab is None or lab.user_id != auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lab not found"
        )

    return lab


@router.delete(
    "/{lab_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove Lab",
)
def destroy_lab(
    lab_id: int,
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    lab_repo = LabInstanceRepository(db)
    lab = lab_repo.get_by_id(lab_id)

    if lab is None or lab.user_id != auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lab not found"
        )

    if lab.status in {"removed", "expired"}:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Lab is already {lab.status}",
        )

    # Matar el procés ttyd abans d'eliminar els contenidors
    ttyd_manager = TtydManager()
    pid = ttyd_process_registry.get_pid(lab_id) or lab.terminal_pid
    if pid:
        ttyd_manager.stop_terminal(pid)
        ttyd_process_registry.unregister(lab_id)
        print(f"[ttyd] Stopped for lab {lab_id} (pid {pid})")

    docker_client = get_docker_client()
    provisioner = LabProvisioner(docker_client)
    provisioner.cleanup(
        containers_info=lab.containers_info,
        networks_info=lab.networks_info,
    )

    lab.status = "removed"
    lab_repo.update(lab)

    return None


# validar flag
@router.post("/{lab_id}/submit", response_model=FlagSubmitResponse)
def submit_flag(
    lab_id: int,
    payload: FlagSubmitRequest,
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    lab_repo = LabInstanceRepository(db)
    lab = lab_repo.get_by_id(lab_id)

    if lab is None or lab.user_id != auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab not found",
        )

    if lab.status != "running":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El laboratori no està actiu",
        )

    if lab.flag_value is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Aquest laboratori no té flag configurada",
        )

    submission_repo = SubmissionRepository(db)
    existing_correct = submission_repo.get_correct_by_user_and_scenario(
        auth_user.id,
        lab.scenario_id,
    )
    if existing_correct:
        return FlagSubmitResponse(
            correct=True,
            message="Aquest escenari ja estava completat anteriorment.",
        )

    submitted = payload.flag.strip()
    expected = lab.flag_value.strip()
    is_correct = submitted.lower() == expected.lower()

    # Calcular temps des de l'inici del lab
    time_seconds = None
    if is_correct and lab.created_at:
        now = datetime.now(timezone.utc)
        time_seconds = int((now - lab.created_at).total_seconds())

    # Guardar submission
    submission = Submission(
        user_id=auth_user.id,
        scenario_id=lab.scenario_id,
        lab_instance_id=lab.id,
        submitted_flag=submitted,
        is_correct=is_correct,
    )
    submission_repo.create(submission)

    # Actualitzar progrés
    progress_repo = UserProgressRepository(db)
    progress_repo.upsert(
        user_id=auth_user.id,
        scenario_id=lab.scenario_id,
        success=is_correct,
        time_seconds=time_seconds,
    )

    if is_correct:
        return FlagSubmitResponse(
            correct=True,
            message="Flag correcta! Has completat l'escenari.",
        )
    else:
        return FlagSubmitResponse(
            correct=False,
            message="Flag incorrecta. Torna-ho a intentar.",
        )

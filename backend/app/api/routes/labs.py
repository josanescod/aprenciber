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

    lab = LabInstance(
        user_id=auth_user.id,
        scenario_id=scenario.id,
        status=lab_data["status"],
        containers_info=lab_data["containers_info"],
        networks_info=lab_data["networks_info"],
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    )

    saved_lab = lab_repo.create(lab)
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

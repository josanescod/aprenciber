from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import zipfile
import io


from app.dependencies.db import get_db
from app.dependencies.auth import get_current_auth_user, require_admin
from app.schemas.scenario import ScenarioOut, ScenarioDetail, ScenarioAdminOut
from app.services.scenario_service import ScenarioService
from app.services.auth_provider import AuthenticatedUser
from app.infrastructure.scenarios.scenario_loader import (
    sync_scenarios_to_db,
    SCENARIOS_DIR,
)
from app.infrastructure.docker.lab_provisioner import LabProvisioner
from app.infrastructure.docker.docker_client import get_docker_client

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.get("", response_model=list[ScenarioOut])
def list_scenarios(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_auth_user),
):
    service = ScenarioService(db)
    return service.list_active_scenarios()


@router.get("/{scenario_id}", response_model=ScenarioDetail)
def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_auth_user),
):
    service = ScenarioService(db)
    return service.get_scenario(scenario_id)


@router.get("/admin/all", response_model=list[ScenarioAdminOut])
def list_all_scenarios(
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(require_admin),
):
    service = ScenarioService(db)
    return service.list_all_scenarios()


@router.patch("/admin/{scenario_id}/toggle", response_model=ScenarioAdminOut)
def toggle_scenario_active(
    scenario_id: int,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(require_admin),
):
    service = ScenarioService(db)
    return service.toggle_active(scenario_id)


# mètode per pujar fitxers d'escenaris en format zip
@router.post("/admin/upload", status_code=201)
def upload_scenario(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(require_admin),
):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="El fitxer ha de ser un .zip")

    contents = file.file.read()

    try:
        zf = zipfile.ZipFile(io.BytesIO(contents))
    except zipfile.BadZipFile as exc:
        raise HTTPException(status_code=400, detail="Fitxer ZIP invàlid") from exc

    with zf:
        names = zf.namelist()
        if not any("scenario.yaml" in n for n in names):
            raise HTTPException(
                status_code=400, detail="El ZIP ha de contenir un fitxer scenario.yaml"
            )
        zf.extractall(SCENARIOS_DIR)

    # Sincronitzar escenaris a la BD
    count = sync_scenarios_to_db(db)

    # Construir imatges Docker dels nous escenaris
    try:
        from app.infrastructure.scenarios.scenario_loader import load_all_scenarios

        docker_client = get_docker_client()
        provisioner = LabProvisioner(docker_client)
        scenarios = load_all_scenarios()
        for scenario in scenarios:
            scenario_path = Path(scenario.yaml_path).parent
            for container in scenario.containers.values():
                if container.build_context:
                    provisioner._ensure_image_exists(
                        image=container.image,
                        scenario_path=scenario_path,
                        build_context=container.build_context,
                        dockerfile=container.dockerfile,
                    )
    except Exception as e:
        print(f"[upload] Warning: error construint imatges: {e}")

    return {
        "message": f"Escenari carregat correctament. {count} escenaris sincronitzats."
    }

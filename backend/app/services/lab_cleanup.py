import asyncio
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.docker.docker_client import get_docker_client
from app.infrastructure.docker.lab_provisioner import LabProvisioner
from app.models.lab_instance import LabInstance


async def cleanup_expired_labs_loop():

    docker_client = get_docker_client()
    provisioner = LabProvisioner(docker_client)

    while True:
        db: Session = SessionLocal()

        try:
            now = datetime.now(timezone.utc)

            expired_labs = (
                db.query(LabInstance)
                .filter(
                    LabInstance.status == "running",
                    LabInstance.expires_at < now,
                )
                .all()
            )

            if expired_labs:
                print(f"[cleanup] Found {len(expired_labs)} expired labs")

            for lab in expired_labs:
                try:
                    provisioner.cleanup(
                        containers_info=lab.containers_info,
                        networks_info=lab.networks_info,
                    )

                    lab.status = "expired"
                    db.add(lab)
                    db.commit()

                    print(f"[cleanup] Lab {lab.id} expired and removed")

                except Exception as e:
                    print(f"[cleanup] Error cleaning lab {lab.id}: {e}")

        finally:
            db.close()

        await asyncio.sleep(30)  # cada 30 segons

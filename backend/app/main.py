from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from app.api.routes.labs import router as labs_router
from app.api.routes.scenarios import router as scenarios_router
from app.api.routes.users import router as users_router
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.scenarios.scenario_loader import sync_scenarios_to_db
from app.services.lab_cleanup import cleanup_expired_labs_loop
from app.api.routes.progress import router as progress_router
from app.api.routes.classrooms import router as classrooms_router
from app.infrastructure.auth.supabase_auth_service import SupabaseAuthService
from app.repositories.profile_repository import ProfileRepository
from app.models.profile import Profile
from app.core.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db = SessionLocal()
    cleanup_task = None
    try:
        # Crear admin per defecte si no existeix
        try:
            profile_repo = ProfileRepository()
            existing = db.query(Profile).filter_by(role="admin").first()
            if not existing:
                supabase = SupabaseAuthService()
                auth_user = supabase.create_user(
                    email=settings.default_admin_email,
                    password=settings.default_admin_password,
                    full_name=settings.default_admin_name,
                )
                profile_repo.create(
                    db,
                    profile_id=auth_user.id,
                    email=settings.default_admin_email,
                    full_name=settings.default_admin_name,
                    role="admin",
                )
                print(
                    f"[startup] admin per defecte creat: {settings.default_admin_email}"
                )
            else:
                print("[startup] admin ja existeix, no es crea un de nou")
        except Exception as exc:
            print(f"[startup] Error creant admin per defecte: {exc}")

        # Sincronitzar escenaris
        try:
            count = sync_scenarios_to_db(db)
            print(f"[startup] {count} scenarios synchronized from YAML")
        except (SQLAlchemyError, ValueError, FileNotFoundError) as exc:
            print(f"[startup] Error synchronizing scenarios: {exc}")

        cleanup_task = asyncio.create_task(cleanup_expired_labs_loop())
        yield
    finally:
        if cleanup_task:
            cleanup_task.cancel()
            try:
                await cleanup_task
            except asyncio.CancelledError:
                pass
        db.close()


app = FastAPI(title="AprenCiber API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(scenarios_router)
app.include_router(labs_router)
app.include_router(progress_router)
app.include_router(classrooms_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

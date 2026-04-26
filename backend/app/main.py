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


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    cleanup_task = None

    try:
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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(scenarios_router)
app.include_router(labs_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

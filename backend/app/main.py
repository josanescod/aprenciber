from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.users import router as users_router
from app.api.routes.scenarios import router as scenarios_router

from app.infrastructure.scenarios.scenario_loader import sync_scenarios_to_db
from app.infrastructure.db.session import SessionLocal

from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title="AprenCiber API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_sync_scenarios():
    db = SessionLocal()
    try:
        count = sync_scenarios_to_db(db)
        print(f"[startup] {count} scenarios synchronized from YAML")
    except (SQLAlchemyError, ValueError, FileNotFoundError) as exc:
        print(f"[startup] Error synchronizing scenarios:: {exc}")
    finally:
        db.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(scenarios_router)

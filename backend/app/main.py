from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import api_router
from backend.app.core.config import settings
from backend.app.db.session import Base, engine


app = FastAPI(
    title="Universal Clinic Workflow Orchestrator",
    version="0.1.0",
    description="Reliability layer for clinic workflow automation across heterogeneous EHR interfaces.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


app.include_router(api_router, prefix="/api")

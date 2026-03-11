from fastapi import APIRouter

from backend.app.api import dashboard, handoffs, runs, seed, settings, simulators, templates


api_router = APIRouter()
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(handoffs.router, prefix="/handoffs", tags=["handoffs"])
api_router.include_router(simulators.router, prefix="/simulators", tags=["simulators"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(seed.router, prefix="/seed", tags=["seed"])

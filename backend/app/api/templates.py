from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import WorkflowTemplate
from backend.app.services.workflow_engine import WorkflowEngine


router = APIRouter()


@router.post("/sync")
def sync_templates(db: Session = Depends(get_db)) -> dict:
    WorkflowEngine().sync_templates(db)
    return {"status": "ok"}


@router.get("")
def list_templates(db: Session = Depends(get_db)) -> list[dict]:
    templates = db.execute(select(WorkflowTemplate)).scalars().all()
    return [
        {"id": item.id, "name": item.name, "slug": item.slug, "version": item.version, "definition": item.definition}
        for item in templates
    ]

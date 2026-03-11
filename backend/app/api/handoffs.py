from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import HandoffItem


router = APIRouter()


@router.get("")
def list_handoffs(db: Session = Depends(get_db)) -> list[dict]:
    items = db.execute(select(HandoffItem).order_by(desc(HandoffItem.created_at))).scalars().all()
    return [
        {
            "id": item.id,
            "workflow_run_id": item.workflow_run_id,
            "status": item.status,
            "priority": item.priority,
            "reason": item.reason,
            "redacted_context": item.redacted_context,
            "created_at": item.created_at,
        }
        for item in items
    ]

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import HandoffItem, WorkflowRun, WorkflowTemplate, Clinic
from backend.app.schemas.workflows import DashboardResponse
from backend.app.services.dashboard import DashboardService


router = APIRouter()


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)) -> DashboardResponse:
    service = DashboardService()
    active_runs = db.execute(
        select(WorkflowRun, WorkflowTemplate, Clinic)
        .join(WorkflowTemplate, WorkflowRun.template_id == WorkflowTemplate.id)
        .join(Clinic, WorkflowRun.clinic_id == Clinic.id)
        .order_by(desc(WorkflowRun.created_at))
        .limit(10)
    ).all()
    handoff_queue = db.execute(select(HandoffItem).order_by(desc(HandoffItem.created_at)).limit(10)).scalars().all()
    return DashboardResponse(
        metrics=service.get_overview(db),
        active_runs=[
            {
                "id": run.id,
                "template_name": template.name,
                "clinic_name": clinic.name,
                "status": run.status,
                "outcome": run.outcome,
                "confidence": run.confidence,
                "current_step": run.current_step,
                "created_at": run.created_at,
            }
            for run, template, clinic in active_runs
        ],
        failures_by_reason=service.get_failures(db),
        handoff_queue=[
            {
                "id": item.id,
                "status": item.status,
                "priority": item.priority,
                "reason": item.reason,
                "created_at": item.created_at,
            }
            for item in handoff_queue
        ],
        workflows=service.get_workflows(db),
        simulators=service.get_simulators(db),
    )

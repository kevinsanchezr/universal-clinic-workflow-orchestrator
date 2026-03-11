from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import Clinic, ExecutionStep, WorkflowRun, WorkflowTemplate
from backend.app.schemas.workflows import WorkflowLaunchRequest, WorkflowRunDetail, WorkflowRunSummary
from backend.app.services.workflow_engine import WorkflowEngine


router = APIRouter()


@router.get("", response_model=list[WorkflowRunSummary])
def list_runs(db: Session = Depends(get_db)) -> list[WorkflowRunSummary]:
    rows = db.execute(
        select(WorkflowRun, WorkflowTemplate, Clinic)
        .join(WorkflowTemplate, WorkflowRun.template_id == WorkflowTemplate.id)
        .join(Clinic, WorkflowRun.clinic_id == Clinic.id)
        .order_by(desc(WorkflowRun.created_at))
    ).all()
    return [
        WorkflowRunSummary(
            id=run.id,
            template_name=template.name,
            clinic_name=clinic.name,
            status=run.status,
            outcome=run.outcome,
            confidence=run.confidence,
            current_step=run.current_step,
            created_at=run.created_at,
        )
        for run, template, clinic in rows
    ]


@router.post("")
def launch_workflow(request: WorkflowLaunchRequest, db: Session = Depends(get_db)) -> dict:
    engine = WorkflowEngine()
    engine.sync_templates(db)
    template = db.scalar(select(WorkflowTemplate).where(WorkflowTemplate.slug == request.template_slug))
    if not template:
        raise HTTPException(status_code=404, detail="Workflow template not found")

    run = engine.create_run(db, request.clinic_id, template, request.requested_by_user_id, request.ehr_style, request.payload)
    run = engine.execute_run(db, run, template, request.payload)
    return {"run_id": run.id, "status": run.status, "outcome": run.outcome}


@router.get("/{run_id}", response_model=WorkflowRunDetail)
def get_run(run_id: str, db: Session = Depends(get_db)) -> WorkflowRunDetail:
    run = db.scalar(select(WorkflowRun).where(WorkflowRun.id == run_id))
    if not run:
        raise HTTPException(status_code=404, detail="Workflow run not found")
    steps = db.execute(select(ExecutionStep).where(ExecutionStep.workflow_run_id == run.id).order_by(ExecutionStep.created_at.asc())).scalars().all()
    return WorkflowRunDetail(
        id=run.id,
        status=run.status,
        outcome=run.outcome,
        confidence=run.confidence,
        ehr_style=run.ehr_style,
        current_step=run.current_step,
        redacted_input=run.redacted_input,
        state_snapshot=run.state_snapshot,
        steps=[
            {
                "id": step.id,
                "step_key": step.step_key,
                "status": step.status,
                "action_type": step.action_type,
                "confidence": step.confidence,
                "rationale": step.rationale,
                "retry_count": step.retry_count,
                "input_summary": step.input_summary,
                "output_summary": step.output_summary,
                "adapter_trace": step.adapter_trace,
                "created_at": step.created_at,
            }
            for step in steps
        ],
    )

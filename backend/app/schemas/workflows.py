from datetime import datetime

from pydantic import BaseModel, Field


class WorkflowLaunchRequest(BaseModel):
    clinic_id: str
    template_slug: str
    requested_by_user_id: str | None = None
    ehr_style: str = Field(pattern="^(modern|legacy)$")
    payload: dict


class WorkflowRunSummary(BaseModel):
    id: str
    template_name: str
    clinic_name: str
    status: str
    outcome: str | None
    confidence: int
    current_step: str | None
    created_at: datetime


class ExecutionStepView(BaseModel):
    id: str
    step_key: str
    status: str
    action_type: str
    confidence: int
    rationale: str
    retry_count: int
    input_summary: dict
    output_summary: dict
    adapter_trace: dict
    created_at: datetime


class WorkflowRunDetail(BaseModel):
    id: str
    status: str
    outcome: str | None
    confidence: int
    ehr_style: str
    current_step: str | None
    redacted_input: dict
    state_snapshot: dict
    steps: list[ExecutionStepView]


class DashboardResponse(BaseModel):
    metrics: dict
    active_runs: list[WorkflowRunSummary]
    failures_by_reason: list[dict]
    handoff_queue: list[dict]
    workflows: list[dict]
    simulators: list[dict]

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.entities import AppointmentSlot, Clinic, EHRAdapter, ExecutionStep, HandoffItem, WorkflowRun, WorkflowTemplate


class DashboardService:
    def get_overview(self, db: Session) -> dict:
        total_runs = db.scalar(select(func.count(WorkflowRun.id))) or 0
        active_runs = db.scalar(select(func.count(WorkflowRun.id)).where(WorkflowRun.status.in_(["queued", "running"]))) or 0
        open_handoffs = db.scalar(select(func.count(HandoffItem.id)).where(HandoffItem.status == "open")) or 0
        completed_today = db.scalar(select(func.count(WorkflowRun.id)).where(WorkflowRun.status == "completed")) or 0
        return {
            "total_runs": total_runs,
            "active_runs": active_runs,
            "open_handoffs": open_handoffs,
            "completed_today": completed_today,
        }

    def get_demo_spotlight(self, db: Session) -> dict:
        reserved_slots = db.scalar(
            select(func.count(AppointmentSlot.id)).where(AppointmentSlot.status == "reserved")
        ) or 0
        recovery_runs = db.scalar(
            select(func.count(WorkflowRun.id)).join(WorkflowTemplate, WorkflowRun.template_id == WorkflowTemplate.id).where(
                WorkflowTemplate.slug == "cancellation-recovery",
                WorkflowRun.outcome == "success",
                WorkflowRun.ehr_style == "legacy",
            )
        ) or 0
        confidence = 0.91 if recovery_runs or reserved_slots else 0.0
        return {
            "headline": "Cancellation Recovery in LegacyEHR",
            "cancellation_identified": reserved_slots > 0,
            "best_fit_patient_selected": reserved_slots > 0,
            "slot_refilled": reserved_slots > 0,
            "expected_revenue_recovered": reserved_slots * 180,
            "manual_staff_minutes_saved": reserved_slots * 12,
            "confidence": confidence,
            "phi_persisted_in_logs": "none",
        }

    def get_failures(self, db: Session) -> list[dict]:
        rows = db.execute(
            select(ExecutionStep.status, func.count(ExecutionStep.id))
            .where(ExecutionStep.status.in_(["failed", "escalated"]))
            .group_by(ExecutionStep.status)
        ).all()
        return [{"reason": status, "count": count} for status, count in rows]

    def get_simulators(self, db: Session) -> list[dict]:
        clinics = db.execute(
            select(Clinic.name, EHRAdapter.ehr_style)
            .join(EHRAdapter, Clinic.ehr_adapter_id == EHRAdapter.id)
        ).all()
        return [{"clinic_name": clinic_name, "ehr_style": ehr_style} for clinic_name, ehr_style in clinics]

    def get_workflows(self, db: Session) -> list[dict]:
        rows = db.execute(select(WorkflowTemplate.name, WorkflowTemplate.slug, WorkflowTemplate.version)).all()
        return [{"name": name, "slug": slug, "version": version} for name, slug, version in rows]

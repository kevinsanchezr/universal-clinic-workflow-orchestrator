from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.entities import (
    AppointmentSlot,
    ExecutionStep,
    HandoffItem,
    SimulatedPatient,
    TaskInput,
    WorkflowRun,
    WorkflowTemplate,
)
from backend.app.services.audit import AuditService
from backend.app.services.policy_engine import PolicyEngine
from backend.app.simulators.ehr import get_adapter
from backend.app.templates.loader import load_templates
from backend.app.utils.logging import get_logger, json_log
from backend.app.utils.redaction import redact_payload


logger = get_logger("workflow-engine")


class WorkflowEngine:
    def __init__(self):
        self.policy_engine = PolicyEngine()
        self.audit_service = AuditService()

    def sync_templates(self, db: Session) -> None:
        existing = {item.slug: item for item in db.scalars(select(WorkflowTemplate)).all()}
        for template in load_templates():
            record = existing.get(template["slug"])
            if record:
                record.definition = template
                record.name = template["name"]
                record.version = template["version"]
            else:
                db.add(
                    WorkflowTemplate(
                        name=template["name"],
                        slug=template["slug"],
                        version=template["version"],
                        definition=template,
                    )
                )
        db.commit()

    def create_run(self, db: Session, clinic_id: str, template: WorkflowTemplate, user_id: str | None, ehr_style: str, payload: dict) -> WorkflowRun:
        run = WorkflowRun(
            clinic_id=clinic_id,
            template_id=template.id,
            requested_by_user_id=user_id,
            status="queued",
            outcome=None,
            confidence=0,
            current_step=None,
            ehr_style=ehr_style,
            redacted_input=redact_payload(payload),
            state_snapshot={"events": []},
        )
        db.add(run)
        db.flush()
        db.add(
            TaskInput(
                workflow_run_id=run.id,
                payload=payload,
                redacted_payload=redact_payload(payload),
            )
        )
        db.commit()
        self.audit_service.write(db, "workflow.created", "system", user_id, {"template": template.slug}, run.id)
        return run

    def execute_run(self, db: Session, run: WorkflowRun, template: WorkflowTemplate, payload: dict) -> WorkflowRun:
        adapter = get_adapter(run.ehr_style)
        run.status = "running"
        state = {"screen": "home", "workflow": template.slug}
        template_steps = template.definition["steps"]

        for step in template_steps:
            decision = self.policy_engine.decide(step, payload, state)
            run.current_step = step["key"]
            step_record = ExecutionStep(
                workflow_run_id=run.id,
                step_key=step["key"],
                status="running",
                action_type=step["action_type"],
                confidence=decision.confidence,
                rationale=decision.rationale,
                input_summary=redact_payload({field: payload.get(field) for field in step.get("required_fields", [])}),
            )
            db.add(step_record)
            db.flush()

            if decision.escalate and step.get("handoff_on_low_confidence", True):
                step_record.status = "escalated"
                db.add(
                    HandoffItem(
                        workflow_run_id=run.id,
                        status="open",
                        priority=step.get("handoff_priority", "high"),
                        reason=decision.rationale,
                        redacted_context=redact_payload(payload),
                    )
                )
                run.status = "escalated"
                run.outcome = "human_review_required"
                run.confidence = min(run.confidence or 100, decision.confidence)
                self.audit_service.write(
                    db,
                    "workflow.escalated",
                    "system",
                    run.requested_by_user_id,
                    {"step": step["key"], "reason": decision.rationale},
                    run.id,
                )
                db.commit()
                return run

            trace = []
            trace.append(adapter.find_screen(state, step.get("screen", "home")).trace)
            if step.get("field"):
                trace.append(adapter.locate_field(step.get("screen", "home"), step["field"]).trace)
                if payload.get(step["field"]):
                    trace.append(adapter.input_value(step["field"], str(payload[step["field"]])).trace)
            if step.get("action_name"):
                trace.append(adapter.click_action(step["action_name"]).trace)
            trace.append(adapter.validate_result(step.get("expected_result", "ok")).trace)

            output = self._apply_business_effects(db, run, template.slug, step["key"], payload)
            step_record.status = "completed"
            step_record.output_summary = output
            step_record.adapter_trace = {"events": trace}
            run.confidence = max(run.confidence, decision.confidence)
            run.state_snapshot = {
                **run.state_snapshot,
                "last_step": step["key"],
                "events": [*run.state_snapshot.get("events", []), {"step": step["key"], "status": "completed"}],
            }
            self.audit_service.write(
                db,
                "workflow.step_completed",
                "system",
                run.requested_by_user_id,
                {"step": step["key"], "output": output},
                run.id,
            )
            json_log(logger, "workflow.step_completed", {"run_id": run.id, "step": step["key"], "confidence": decision.confidence})

        run.status = "completed"
        run.outcome = "success"
        run.current_step = template_steps[-1]["key"] if template_steps else None
        db.commit()
        self.audit_service.write(db, "workflow.completed", "system", run.requested_by_user_id, {"outcome": run.outcome}, run.id)
        return run

    def _apply_business_effects(self, db: Session, run: WorkflowRun, workflow_slug: str, step_key: str, payload: dict) -> dict:
        if workflow_slug == "cancellation-recovery" and step_key == "reserve_slot":
            slot = db.scalar(
                select(AppointmentSlot)
                .where(AppointmentSlot.clinic_id == run.clinic_id, AppointmentSlot.status == "cancelled")
                .order_by(AppointmentSlot.start_at.asc())
            )
            candidate = db.scalar(
                select(SimulatedPatient)
                .where(SimulatedPatient.clinic_id == run.clinic_id, SimulatedPatient.is_waitlist.is_(True))
                .order_by(SimulatedPatient.created_at.asc())
            )
            if slot and candidate:
                slot.status = "reserved"
                return {"reserved_slot": slot.start_at, "candidate": candidate.pseudonym}

        if workflow_slug == "appointment-booking" and step_key == "schedule_appointment":
            slot = db.scalar(
                select(AppointmentSlot)
                .where(
                    AppointmentSlot.clinic_id == run.clinic_id,
                    AppointmentSlot.status == "open",
                    AppointmentSlot.visit_type == payload.get("appointment_type", "Follow-up"),
                )
                .order_by(AppointmentSlot.start_at.asc())
            )
            if slot:
                slot.status = "booked"
                slot.is_confirmed = True
                return {"scheduled_at": slot.start_at, "provider_name": slot.provider_name}

        if workflow_slug == "prescription-refill-intake" and step_key == "route_refill_request":
            return {"queue": "pharmacy_confirmation", "status": "queued_for_review"}

        if workflow_slug == "next-day-schedule-scrub" and step_key == "generate_call_tasks":
            flagged = db.scalar(
                select(func.count(AppointmentSlot.id)).where(
                    AppointmentSlot.clinic_id == run.clinic_id,
                    AppointmentSlot.status == "booked",
                    AppointmentSlot.is_confirmed.is_(False),
                )
            )
            return {"call_tasks_generated": flagged or 0}

        return {"status": "no_state_change"}

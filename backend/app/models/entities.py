from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.session import Base
from backend.app.models.base import TimestampMixin, UUIDMixin


JSONType = JSONB().with_variant(JSONB, "postgresql")


class Clinic(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "clinics"

    name: Mapped[str] = mapped_column(String(255), index=True)
    segment: Mapped[str] = mapped_column(String(64), index=True)
    timezone: Mapped[str] = mapped_column(String(64), default="America/New_York")
    ehr_adapter_id: Mapped[str | None] = mapped_column(ForeignKey("ehr_adapters.id"))

    users = relationship("User", back_populates="clinic")
    workflow_runs = relationship("WorkflowRun", back_populates="clinic")
    simulated_patients = relationship("SimulatedPatient", back_populates="clinic")
    appointment_slots = relationship("AppointmentSlot", back_populates="clinic")


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    clinic_id: Mapped[str] = mapped_column(ForeignKey("clinics.id"), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(64), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    clinic = relationship("Clinic", back_populates="users")


class EHRAdapter(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "ehr_adapters"

    name: Mapped[str] = mapped_column(String(128), unique=True)
    vendor: Mapped[str] = mapped_column(String(128))
    ehr_style: Mapped[str] = mapped_column(String(64), index=True)
    capabilities: Mapped[dict] = mapped_column(JSONType, default=dict)


class WorkflowTemplate(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "workflow_templates"

    name: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    definition: Mapped[dict] = mapped_column(JSONType)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    runs = relationship("WorkflowRun", back_populates="template")


class WorkflowRun(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "workflow_runs"
    __table_args__ = (
        Index("ix_workflow_runs_clinic_status", "clinic_id", "status"),
        Index("ix_workflow_runs_template_status", "template_id", "status"),
    )

    clinic_id: Mapped[str] = mapped_column(ForeignKey("clinics.id"), index=True)
    template_id: Mapped[str] = mapped_column(ForeignKey("workflow_templates.id"), index=True)
    requested_by_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    outcome: Mapped[str | None] = mapped_column(String(64), index=True)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    current_step: Mapped[str | None] = mapped_column(String(128))
    ehr_style: Mapped[str] = mapped_column(String(64))
    redacted_input: Mapped[dict] = mapped_column(JSONType)
    state_snapshot: Mapped[dict] = mapped_column(JSONType, default=dict)

    clinic = relationship("Clinic", back_populates="workflow_runs")
    template = relationship("WorkflowTemplate", back_populates="runs")
    steps = relationship("ExecutionStep", back_populates="run", cascade="all, delete-orphan")
    handoff_items = relationship("HandoffItem", back_populates="run")


class TaskInput(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "task_inputs"

    workflow_run_id: Mapped[str] = mapped_column(ForeignKey("workflow_runs.id"), index=True)
    schema_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    payload: Mapped[dict] = mapped_column(JSONType)
    redacted_payload: Mapped[dict] = mapped_column(JSONType)


class ExecutionStep(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "execution_steps"
    __table_args__ = (Index("ix_execution_steps_run_step", "workflow_run_id", "step_key"),)

    workflow_run_id: Mapped[str] = mapped_column(ForeignKey("workflow_runs.id"), index=True)
    step_key: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), index=True)
    action_type: Mapped[str] = mapped_column(String(64))
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    rationale: Mapped[str] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    input_summary: Mapped[dict] = mapped_column(JSONType, default=dict)
    output_summary: Mapped[dict] = mapped_column(JSONType, default=dict)
    adapter_trace: Mapped[dict] = mapped_column(JSONType, default=dict)

    run = relationship("WorkflowRun", back_populates="steps")


class HandoffItem(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "handoff_items"
    __table_args__ = (Index("ix_handoff_items_status_priority", "status", "priority"),)

    workflow_run_id: Mapped[str] = mapped_column(ForeignKey("workflow_runs.id"), index=True)
    assigned_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    priority: Mapped[str] = mapped_column(String(32), index=True)
    reason: Mapped[str] = mapped_column(Text)
    redacted_context: Mapped[dict] = mapped_column(JSONType, default=dict)

    run = relationship("WorkflowRun", back_populates="handoff_items")


class AuditLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_run_event", "workflow_run_id", "event_type"),)

    workflow_run_id: Mapped[str | None] = mapped_column(ForeignKey("workflow_runs.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    actor_type: Mapped[str] = mapped_column(String(32))
    actor_id: Mapped[str | None] = mapped_column(String(128))
    payload: Mapped[dict] = mapped_column(JSONType, default=dict)
    checksum: Mapped[str] = mapped_column(String(128), index=True)


class SimulatedPatient(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "simulated_patients"
    __table_args__ = (
        Index("ix_simulated_patients_clinic_waitlist", "clinic_id", "is_waitlist"),
        Index("ix_simulated_patients_clinic_pseudo", "clinic_id", "pseudonym"),
    )

    clinic_id: Mapped[str] = mapped_column(ForeignKey("clinics.id"), index=True)
    pseudonym: Mapped[str] = mapped_column(String(255), index=True)
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    callback_number: Mapped[str | None] = mapped_column(String(32))
    insurance_status: Mapped[str | None] = mapped_column(String(64))
    risk_flags: Mapped[dict] = mapped_column(JSONType, default=dict)
    is_waitlist: Mapped[bool] = mapped_column(Boolean, default=False)

    clinic = relationship("Clinic", back_populates="simulated_patients")


class AppointmentSlot(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "appointment_slots"
    __table_args__ = (
        Index("ix_appointment_slots_clinic_datetime", "clinic_id", "start_at"),
        Index("ix_appointment_slots_status_type", "status", "visit_type"),
    )

    clinic_id: Mapped[str] = mapped_column(ForeignKey("clinics.id"), index=True)
    patient_id: Mapped[str | None] = mapped_column(ForeignKey("simulated_patients.id"), index=True)
    start_at: Mapped[str] = mapped_column(String(64), index=True)
    provider_name: Mapped[str] = mapped_column(String(255))
    specialty: Mapped[str] = mapped_column(String(128))
    visit_type: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), index=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    clinic = relationship("Clinic", back_populates="appointment_slots")


class RefillRequest(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "refill_requests"
    __table_args__ = (Index("ix_refill_requests_clinic_status", "clinic_id", "status"),)

    clinic_id: Mapped[str] = mapped_column(ForeignKey("clinics.id"), index=True)
    patient_id: Mapped[str] = mapped_column(ForeignKey("simulated_patients.id"), index=True)
    medication_name: Mapped[str] = mapped_column(String(255))
    pharmacy_name: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), index=True)
    urgency: Mapped[str] = mapped_column(String(32), default="routine")
    requires_handoff: Mapped[bool] = mapped_column(Boolean, default=False)


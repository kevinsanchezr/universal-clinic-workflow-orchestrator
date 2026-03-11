from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.entities import AppointmentSlot, Clinic, EHRAdapter, RefillRequest, SimulatedPatient, User
from backend.app.services.workflow_engine import WorkflowEngine


def seed_demo_data(db: Session) -> dict:
    WorkflowEngine().sync_templates(db)
    if db.scalar(select(Clinic.id).limit(1)):
        return {"seeded": False, "reason": "data already present"}

    modern = EHRAdapter(
        name="ModernEHR Adapter",
        vendor="ModernEHR",
        ehr_style="modern",
        capabilities={"selectors": True, "semantic_fallback": True},
    )
    legacy = EHRAdapter(
        name="LegacyEHR Adapter",
        vendor="LegacySuite",
        ehr_style="legacy",
        capabilities={"selectors": True, "semantic_fallback": True, "ocr": False},
    )
    db.add_all([modern, legacy])
    db.flush()

    clinics = [
        Clinic(name="Harbor Family Practice", segment="solo", ehr_adapter_id=modern.id),
        Clinic(name="Northside Wellness Boutique", segment="boutique", ehr_adapter_id=modern.id),
        Clinic(name="Summit Specialty Group", segment="enterprise", ehr_adapter_id=legacy.id),
    ]
    db.add_all(clinics)
    db.flush()

    users = [
        User(clinic_id=clinics[0].id, email="admin@harbor.test", full_name="Avery Quinn", role="admin"),
        User(clinic_id=clinics[1].id, email="ops@northside.test", full_name="Jordan Mills", role="ops_manager"),
        User(clinic_id=clinics[2].id, email="reviewer@summit.test", full_name="Taylor Shaw", role="reviewer"),
    ]
    db.add_all(users)
    db.flush()

    patients = [
        SimulatedPatient(
            clinic_id=clinics[0].id,
            pseudonym="P-001",
            first_name="Mara",
            last_name="Lane",
            callback_number="555-1010",
            insurance_status="verified",
            risk_flags={"language": "en"},
            is_waitlist=True,
        ),
        SimulatedPatient(
            clinic_id=clinics[0].id,
            pseudonym="P-002",
            first_name="Theo",
            last_name="Vale",
            callback_number="555-1011",
            insurance_status="missing",
            risk_flags={"confirmation": "pending"},
            is_waitlist=False,
        ),
        SimulatedPatient(
            clinic_id=clinics[1].id,
            pseudonym="P-101",
            first_name="Nina",
            last_name="Reed",
            callback_number="555-2010",
            insurance_status="verified",
            risk_flags={"preferred_days": ["Mon", "Wed"]},
            is_waitlist=True,
        ),
        SimulatedPatient(
            clinic_id=clinics[2].id,
            pseudonym="P-201",
            first_name="Luca",
            last_name="Stone",
            callback_number="555-3010",
            insurance_status="inactive",
            risk_flags={"enterprise": True},
            is_waitlist=True,
        ),
    ]
    db.add_all(patients)
    db.flush()

    slots = [
        AppointmentSlot(
            clinic_id=clinics[0].id,
            patient_id=patients[1].id,
            start_at="2026-03-11T15:00:00Z",
            provider_name="Dr. Kim",
            specialty="Primary Care",
            visit_type="Follow-up",
            status="cancelled",
            is_confirmed=False,
        ),
        AppointmentSlot(
            clinic_id=clinics[0].id,
            patient_id=None,
            start_at="2026-03-12T09:00:00Z",
            provider_name="Dr. Kim",
            specialty="Primary Care",
            visit_type="Follow-up",
            status="open",
            is_confirmed=False,
        ),
        AppointmentSlot(
            clinic_id=clinics[1].id,
            patient_id=None,
            start_at="2026-03-12T13:00:00Z",
            provider_name="Dr. Shah",
            specialty="Dermatology",
            visit_type="Consult",
            status="open",
            is_confirmed=False,
        ),
        AppointmentSlot(
            clinic_id=clinics[2].id,
            patient_id=patients[3].id,
            start_at="2026-03-11T16:00:00Z",
            provider_name="Dr. Ortiz",
            specialty="Cardiology",
            visit_type="Follow-up",
            status="cancelled",
            is_confirmed=False,
        ),
        AppointmentSlot(
            clinic_id=clinics[2].id,
            patient_id=patients[3].id,
            start_at="2026-03-12T10:00:00Z",
            provider_name="Dr. Ortiz",
            specialty="Cardiology",
            visit_type="Follow-up",
            status="booked",
            is_confirmed=False,
        ),
    ]
    db.add_all(slots)

    refill_requests = [
        RefillRequest(
            clinic_id=clinics[0].id,
            patient_id=patients[0].id,
            medication_name="Lisinopril",
            pharmacy_name="Harbor Pharmacy",
            status="new",
            urgency="routine",
        ),
        RefillRequest(
            clinic_id=clinics[2].id,
            patient_id=patients[3].id,
            medication_name="Atorvastatin",
            pharmacy_name="Summit Rx",
            status="new",
            urgency="high",
            requires_handoff=True,
        ),
    ]
    db.add_all(refill_requests)
    db.commit()

    return {"seeded": True, "clinics": len(clinics), "patients": len(patients), "slots": len(slots)}

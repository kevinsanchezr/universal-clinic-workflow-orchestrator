from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import AppointmentSlot, Clinic, EHRAdapter, SimulatedPatient


router = APIRouter()


@router.get("")
def get_simulator_state(db: Session = Depends(get_db)) -> list[dict]:
    clinics = db.execute(select(Clinic)).scalars().all()
    output = []
    for clinic in clinics:
        adapter = db.scalar(select(EHRAdapter).where(EHRAdapter.id == clinic.ehr_adapter_id))
        patients = db.execute(select(SimulatedPatient).where(SimulatedPatient.clinic_id == clinic.id).limit(5)).scalars().all()
        slots = db.execute(select(AppointmentSlot).where(AppointmentSlot.clinic_id == clinic.id).limit(5)).scalars().all()
        output.append(
            {
                "clinic_id": clinic.id,
                "clinic_name": clinic.name,
                "ehr_style": adapter.ehr_style if adapter else "modern",
                "patients": [{"id": p.id, "pseudonym": p.pseudonym, "is_waitlist": p.is_waitlist} for p in patients],
                "slots": [
                    {"id": s.id, "start_at": s.start_at, "visit_type": s.visit_type, "status": s.status, "confirmed": s.is_confirmed}
                    for s in slots
                ],
            }
        )
    return output

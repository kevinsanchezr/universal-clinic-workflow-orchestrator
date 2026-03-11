from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import Clinic, EHRAdapter, User


router = APIRouter()


@router.get("")
def list_clinics(db: Session = Depends(get_db)) -> list[dict]:
    clinics = db.execute(select(Clinic, EHRAdapter).join(EHRAdapter, Clinic.ehr_adapter_id == EHRAdapter.id)).all()
    users_by_clinic = {}
    for user in db.execute(select(User)).scalars().all():
        users_by_clinic.setdefault(user.clinic_id, []).append(
            {"id": user.id, "full_name": user.full_name, "role": user.role, "email": user.email}
        )

    return [
        {
            "id": clinic.id,
            "name": clinic.name,
            "segment": clinic.segment,
            "timezone": clinic.timezone,
            "ehr_adapter": {
                "id": adapter.id,
                "name": adapter.name,
                "vendor": adapter.vendor,
                "ehr_style": adapter.ehr_style,
            },
            "users": users_by_clinic.get(clinic.id, []),
        }
        for clinic, adapter in clinics
    ]

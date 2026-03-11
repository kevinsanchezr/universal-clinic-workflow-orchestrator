from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.services.seed import seed_demo_data


router = APIRouter()


@router.post("")
def seed(db: Session = Depends(get_db)) -> dict:
    result = seed_demo_data(db)
    return {"status": "ok", **result}

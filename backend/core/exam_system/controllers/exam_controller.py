from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from core.common.utils.response import success
from core.exam_system.services.exam_service import submit_exam

router = APIRouter()


@router.post("/exam/submit")
def submit_exam_api(request: dict, db: Session = Depends(get_db)):
    user_id = request.get("user_id")
    answers = request.get("answers", [])

    result = submit_exam(db, user_id, answers)
    return success(result)
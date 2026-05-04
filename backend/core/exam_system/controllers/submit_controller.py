from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.common.utils.response import success, error
from core.exam_system.services.practice_service import submit_answer
from app.db.database import get_db   # ⭐用你已有的

router = APIRouter()

@router.post("/submit")
def submit(data: dict, db: Session = Depends(get_db)):
    # 参数校验
    for key in ["user_id", "question_id", "answer"]:
        if key not in data:
            return error(f"missing {key}")

    result = submit_answer(db, data)

    if result is None:
        return error("question not found")

    return success(result)
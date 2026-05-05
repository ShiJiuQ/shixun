from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from core.common.utils.response import success
from core.exam_system.services.wrong_service import get_wrong_list
from core.exam_system.services import wrong_service

from core.exam_system.services.wrong_service import submit_wrong_practice,get_wrong_practice

router = APIRouter()


@router.get("/wrong")
def get_wrong_questions(
    user_id: str = Query(..., description="用户ID"),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    data = get_wrong_list(db, user_id, page, page_size)
    return success(data)

@router.get("/wrong/practice")
def wrong_practice_api(
    user_id: str,
    db: Session = Depends(get_db)
):
    result = get_wrong_practice(db, user_id)
    return success(result)

@router.post("/wrong/submit")
def submit_wrong_api(
    request: dict,
    db: Session = Depends(get_db)
):
    user_id = request.get("user_id")
    answers = request.get("answers", [])

    result = submit_wrong_practice(db, user_id, answers)
    return success(result)
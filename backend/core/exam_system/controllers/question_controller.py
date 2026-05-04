from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from core.common.utils.response import success
from core.exam_system.services.question_service import get_question_list

router = APIRouter()


@router.get("/questions")
def get_questions(
    year: int = Query(None),
    subject: str = Query(None),
    knowledge_point: str = Query(None),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    params = {
        "year": year,
        "subject": subject,
        "knowledge_point": knowledge_point,
        "page": page,
        "page_size": page_size
    }

    result = get_question_list(db, params)
    return success(result)
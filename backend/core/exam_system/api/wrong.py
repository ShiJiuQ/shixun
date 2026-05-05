from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from core.common.utils.response import success
from core.exam_system.services.wrong_service import get_wrong_list

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
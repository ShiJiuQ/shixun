from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from core.common.utils.response import success
from core.exam_system.services.paper_service import get_paper

router = APIRouter()


@router.get("/paper/{year}")
def get_exam_paper(year: int, db: Session = Depends(get_db)):
    data = get_paper(db, year)
    return success(data)
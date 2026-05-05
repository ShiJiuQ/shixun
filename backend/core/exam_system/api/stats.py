from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from core.exam_system.services.stats_service import get_user_stats
from core.common.utils.response import success

router = APIRouter()


@router.get("/stats")
def stats_api(user_id: str, db: Session = Depends(get_db)):
    result = get_user_stats(db, user_id)
    return success(result)
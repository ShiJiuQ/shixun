from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from core.common.utils.response import success, error
from core.exam_system.services import (
    exam_service,
    wrong_service,
)

# 根路由（可添加前缀，比如 /exam-system）
router = APIRouter()

# -------------------------- 试卷相关 --------------------------
@router.get("/paper/{year}")
def get_exam_paper(year: int, db: Session = Depends(get_db)):
    data = exam_service.get_paper(db, year)
    return success(data)

# -------------------------- 题目相关 --------------------------
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
    result = exam_service.get_question_list(db, params)
    return success(result)

# -------------------------- 答题提交相关 --------------------------
@router.post("/exam/submit")
def submit_exam_api(request: dict, db: Session = Depends(get_db)):
    user_id = request.get("user_id")
    answers = request.get("answers", [])
    result = exam_service.submit_exam(db, user_id, answers)
    return success(result)

@router.post("/practice/submit")  # 区分考试提交和练习提交，路径更清晰
def submit_practice_answer(data: dict, db: Session = Depends(get_db)):
    # 参数校验
    for key in ["user_id", "question_id", "answer"]:
        if key not in data:
            return error(f"missing {key}")
    result = exam_service.submit_answer(db, data)
    if result is None:
        return error("question not found")
    return success(result)

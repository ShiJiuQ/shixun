from sqlalchemy import text

def save_record(
    db,
    user_id,
    question_id,
    is_correct,
    score,
    mode,
    paper_id,
    knowledge_point
):
    sql = text("""
        INSERT INTO records
        (user_id, question_id, is_correct, score, mode, paper_id, knowledge_point)
        VALUES
        (:user_id, :question_id, :is_correct, :score, :mode, :paper_id, :knowledge_point)
    """)

    db.execute(sql, {
        "user_id": user_id,
        "question_id": question_id,
        "is_correct": is_correct,
        "score": score,
        "mode": mode,
        "paper_id": paper_id,
        "knowledge_point": knowledge_point
    })

    db.commit()

from core.common.models.record import Record
from core.common.models.question import Question


def get_wrong_records_with_question(db, user_id, offset=0, limit=10):
    """
    返回：[(Record, Question), ...]
    """
    query = (
        db.query(Record, Question)
        .join(Question, Record.question_id == Question.id)
        .filter(
            Record.user_id == user_id,
            Record.is_correct == False,
            Record.mode == "exam"   # 只统计真题模式
        )
        .order_by(Record.created_at.desc())
    )

    total = query.count()
    rows = query.offset(offset).limit(limit).all()

    return total, rows
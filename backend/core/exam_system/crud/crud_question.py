from core.common.models.question import Question


def get_questions(db, year=None, subject=None, knowledge_point=None, offset=0, limit=10):
    query = db.query(Question)

    if year:
        query = query.filter(Question.exam_year == year)

    if subject:
        query = query.filter(Question.subject_name == subject)

    if knowledge_point:
        query = query.filter(Question.knowledge_point == knowledge_point)

    return query.offset(offset).limit(limit).all()


def count_questions(db, year=None, subject=None, knowledge_point=None):
    query = db.query(Question)

    if year:
        query = query.filter(Question.exam_year == year)

    if subject:
        query = query.filter(Question.subject_name == subject)

    if knowledge_point:
        query = query.filter(Question.knowledge_point == knowledge_point)

    return query.count()

def get_paper_by_year(db, year):
    from core.common.models.question import Question

    return db.query(Question)\
        .filter(Question.exam_year == year)\
        .order_by(Question.question_no)\
        .all()

# 在原有 crud_question.py 中补充
def get_question_by_id(db, question_id):
    from core.common.models.question import Question
    return db.query(Question).filter(Question.id == question_id).first()

def insert_record(db, record_data: dict):
    # 兼容 service 层调用的 insert_record 方法
    from core.exam_system.crud.crud_record import save_record
    save_record(
        db,
        user_id=record_data["user_id"],
        question_id=record_data["question_id"],
        is_correct=record_data["is_correct"],
        score=record_data["score"],
        mode=record_data["mode"],
        paper_id=record_data.get("paper_id"),
        knowledge_point=record_data["knowledge_point"]
    )
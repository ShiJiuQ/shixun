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
    from app.models.question import Question

    return db.query(Question)\
        .filter(Question.exam_year == year)\
        .order_by(Question.question_no)\
        .all()
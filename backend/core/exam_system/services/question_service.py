from core.exam_system.dao import question_dao


def get_question_list(db, params: dict):
    page = int(params.get("page", 1))
    page_size = int(params.get("page_size", 10))

    offset = (page - 1) * page_size

    questions = question_dao.get_questions(
        db,
        year=params.get("year"),
        subject=params.get("subject"),
        knowledge_point=params.get("knowledge_point"),
        offset=offset,
        limit=page_size
    )

    total = question_dao.count_questions(
        db,
        year=params.get("year"),
        subject=params.get("subject"),
        knowledge_point=params.get("knowledge_point")
    )

    result_list = []

    for q in questions:
        result_list.append({
            "id": q.id,
            "exam_year": q.exam_year,
            "question_no": q.question_no,
            "question_type": q.question_type,
            "subject_name": q.subject_name,
            "question_content": q.question_content,
            "options": q.options,
            "knowledge_point": q.knowledge_point,
            "images": q.images
        })

    return {
        "total": total,
        "list": result_list
    }
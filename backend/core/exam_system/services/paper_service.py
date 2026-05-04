def get_paper(db, year):
    from core.exam_system.dao.question_dao import get_paper_by_year

    questions = get_paper_by_year(db, year)

    result = []

    for q in questions:
        result.append({
            "id": q.id,
            "question_no": q.question_no,
            "question_type": q.question_type,
            "question_content": q.question_content,
            "options": q.options,
            "score": 1 if q.question_type == "单项选择题" else 10
        })

    return result
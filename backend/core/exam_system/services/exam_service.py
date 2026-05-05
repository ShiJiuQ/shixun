#套卷提交
def submit_exam(db, user_id, answers: list):
    from core.common.models.question import Question
    from core.exam_system.crud.crud_record import save_record

    total_score = 0
    results = []

    for item in answers:
        question_id = item["question_id"]
        user_answer = item["answer"]

        q = db.query(Question).filter(Question.id == question_id).first()

        if not q:
            continue

        # 判题
        is_correct = (user_answer == q.standard_answer)

        if q.question_type == "单项选择题":
            score = 2 if is_correct else 0
        else:
            # ⭐ 主观题先给0（后面可以接大模型）
            score = 0

        total_score += score

        # 存记录
        save_record(
            db=db,
            user_id=user_id,
            question_id=question_id,
            is_correct=is_correct,
            score=score,
            mode="exam",
            paper_id=str(q.exam_year),
            knowledge_point=q.knowledge_point
        )

        results.append({
            "question_id": question_id,
            "is_correct": is_correct,
            "score": score
        })

    return {
        "total_score": total_score,
        "details": results
    }

#试卷信息
def get_paper(db, year):
    from core.exam_system.crud.crud_question import get_paper_by_year

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

from core.common.utils.judge import judge
from core.exam_system.crud import crud_question, crud_record


#练习提交  （刷题）
def submit_answer(conn, data: dict):
    """
    data:
    {
        user_id,
        question_id,
        answer,
        mode='practice' / 'exam'
    }
    """
    # 1. 查题目
    question = crud_question.get_question_by_id(conn, data["question_id"])
    if not question:
        return None

    # 2. 判题
    result = judge(question, data["answer"])

    # 3. 记录入库（统一结构）
    record = {
        "user_id": data["user_id"],
        "question_id": data["question_id"],
        "is_correct": result["is_correct"],
        "score": result["score"],
        "mode": data.get("mode", "practice"),
        "paper_id": data.get("paper_id"),
        "knowledge_point": question.get("knowledge_point")
    }

    crud_record.insert_record(conn, record)

    # 4. 返回给前端（即时反馈）
    return {
        "is_correct": result["is_correct"],
        "score": result["score"],
        "full_score": result["full_score"],
        "correct_answer": question.get("standard_answer"),
        "analysis": question.get("analysis_content"),
        "knowledge_point": question.get("knowledge_point")
    }


#试题信息 （刷题）
def get_question_list(db, params: dict):
    page = int(params.get("page", 1))
    page_size = int(params.get("page_size", 10))

    offset = (page - 1) * page_size

    questions = crud_question.get_questions(
        db,
        year=params.get("year"),
        subject=params.get("subject"),
        knowledge_point=params.get("knowledge_point"),
        offset=offset,
        limit=page_size
    )

    total = crud_question.count_questions(
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
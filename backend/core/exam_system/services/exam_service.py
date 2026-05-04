def submit_exam(db, user_id, answers: list):
    from app.models.question import Question
    from core.exam_system.dao.record_dao import save_record

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
            score = 1 if is_correct else 0
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
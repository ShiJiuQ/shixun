from core.exam_system.crud.crud_record import (
    save_record,
    get_wrong_records_with_question
)


# ⭐ 保存做题记录（给 exam_service 调）
def create_record(
    db,
    user_id,
    question,
    is_correct,
    score,
    mode="exam",
    paper_id=None
):
    save_record(
        db=db,
        user_id=user_id,
        question_id=question.id,
        is_correct=is_correct,
        score=score,
        mode=mode,
        paper_id=paper_id,
        knowledge_point=question.knowledge_point
    )


# ⭐ 获取错题（分页 + 拼装数据）
def get_wrong_list(db, user_id, page=1, size=10):
    offset = (page - 1) * size

    total, rows = get_wrong_records_with_question(
        db, user_id, offset, size
    )

    result = []
    for record, question in rows:
        result.append({
            "question_id": question.id,
            "question_content": question.question_content,
            "options": question.options,
            "correct_answer": question.standard_answer,
            "analysis": question.analysis_content,
            "knowledge_point": question.knowledge_point,
            "last_score": record.score,
            "created_at": record.created_at
        })

    return {
        "total": total,
        "list": result
    }
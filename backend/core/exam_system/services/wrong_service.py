import json
from core.exam_system.crud.crud_record import get_wrong_records_with_question


def get_wrong_list(db, user_id, page=1, page_size=10):
    offset = (page - 1) * page_size

    total, rows = get_wrong_records_with_question(
        db, user_id, offset, page_size
    )

    result = []

    for record, q in rows:
        # 兼容 JSON 字段（防止是字符串）
        options = q.options
        if isinstance(options, str):
            try:
                options = json.loads(options)
            except:
                options = {}

        images = q.images or []
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except:
                images = []

        result.append({
            "question_id": q.id,
            "exam_year": q.exam_year,
            "question_no": q.question_no,
            "question_type": q.question_type,
            "subject_name": q.subject_name,

            "question_content": q.question_content,
            "options": options,
            "images": images,

            "standard_answer": q.standard_answer,
            "analysis_content": q.analysis_content,
            "knowledge_point": q.knowledge_point,

            # 做题记录信息
            "is_correct": record.is_correct,
            "score": record.score,
            "created_at": str(record.created_at)
        })

    return {
        "total": total,
        "list": result
    }

def get_wrong_practice(db, user_id, limit=10):
    total, rows = get_wrong_records_with_question(
        db, user_id, offset=0, limit=limit
    )

    result = []
    for record, question in rows:
        result.append({
            "question_id": question.id,
            "question_content": question.question_content,
            "options": question.options,
            "knowledge_point": question.knowledge_point
        })

    return result

from core.common.utils.judge import judge
from core.exam_system.crud.crud_question import get_question_by_id
from core.exam_system.services.record_service import create_record


def submit_wrong_practice(db, user_id, answers):
    results = []

    for item in answers:
        qid = item["question_id"]
        user_answer = item["answer"]

        q = get_question_by_id(db, qid)

        is_correct = False
        score = 0

        if q.question_type == "单项选择题":
            is_correct = (user_answer == q.standard_answer)
            score = 1 if is_correct else 0

        # ⭐ 注意这里 mode = wrong
        create_record(
            db,
            user_id,
            q,
            is_correct,
            score,
            mode="wrong",
            paper_id=None
        )

        results.append({
            "question_id": qid,
            "is_correct": is_correct,
            "correct_answer": q.standard_answer,
            "analysis": q.analysis_content
        })

    return results
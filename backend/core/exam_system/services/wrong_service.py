import json
from core.exam_system.dao.record_dao import get_wrong_records_with_question


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
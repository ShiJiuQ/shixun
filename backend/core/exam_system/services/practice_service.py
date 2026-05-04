from core.common.utils.judge import judge
from core.exam_system.dao import question_dao, record_dao

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
    question = question_dao.get_question_by_id(conn, data["question_id"])
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

    record_dao.insert_record(conn, record)

    # 4. 返回给前端（即时反馈）
    return {
        "is_correct": result["is_correct"],
        "score": result["score"],
        "full_score": result["full_score"],
        "correct_answer": question.get("standard_answer"),
        "analysis": question.get("analysis_content"),
        "knowledge_point": question.get("knowledge_point")
    }
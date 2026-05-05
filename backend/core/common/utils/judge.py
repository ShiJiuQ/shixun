def judge(question: dict, user_answer: str):
    q_type = question.get("question_type")

    # 单选
    if q_type == "单项选择题":
        correct = user_answer == question.get("standard_answer")
        return {
            "is_correct": correct,
            "score": 2 if correct else 0,
            "full_score": 2
        }

    # 主观题判定接大模型
    return {
        "is_correct": None,
        "score": 0,
        "full_score": question.get("full_score", 10)
    }


# core/common/utils/judge.py 补充
def judge_exam_answer(question, user_answer):
    """统一的考试答题判分逻辑"""
    if not question:
        return {"is_correct": False, "score": 0, "full_score": question.get("full_score", 10)}

    # 单选判分
    if question.question_type == "单项选择题":
        is_correct = (user_answer == question.standard_answer)
        score = 2 if is_correct else 0
    # 主观题（预留大模型判分接口）
    else:
        is_correct = False  # 暂未实现
        score = 0

    return {
        "is_correct": is_correct,
        "score": score,
        "full_score": 1 if question.question_type == "单项选择题" else 10  # 对齐paper_service的分值
    }

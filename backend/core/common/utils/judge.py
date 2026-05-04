def judge(question: dict, user_answer: str):
    q_type = question.get("question_type")

    # 单选：固定 2 分
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

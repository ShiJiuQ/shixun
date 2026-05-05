from sqlalchemy import text


# ⭐ 总体统计
def get_overview_stats(db, user_id):
    sql = text("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct
        FROM records
        WHERE user_id = :user_id AND mode = 'exam'
    """)

    result = db.execute(sql, {"user_id": user_id}).fetchone()

    total = result.total or 0
    correct = result.correct or 0
    accuracy = round(correct / total, 4) if total > 0 else 0

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy
    }


# ⭐ 按知识点统计
def get_knowledge_stats(db, user_id):
    sql = text("""
        SELECT
            knowledge_point,
            COUNT(*) AS total,
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct
        FROM records
        WHERE user_id = :user_id AND mode = 'exam'
        GROUP BY knowledge_point
        ORDER BY total DESC
    """)

    rows = db.execute(sql, {"user_id": user_id}).fetchall()

    result = []
    for row in rows:
        total = row.total or 0
        correct = row.correct or 0
        accuracy = round(correct / total, 4) if total > 0 else 0

        result.append({
            "knowledge_point": row.knowledge_point,
            "total": total,
            "correct": correct,
            "accuracy": accuracy
        })

    return result
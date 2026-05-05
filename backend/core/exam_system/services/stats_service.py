from core.exam_system.crud.crud_stats import (
    get_overview_stats,
    get_knowledge_stats
)


def get_user_stats(db, user_id):
    overview = get_overview_stats(db, user_id)
    knowledge = get_knowledge_stats(db, user_id)

    return {
        "overview": overview,
        "knowledge_stats": knowledge
    }
from sqlalchemy.orm import Session
# ChatMessage 表和 User 表写在了一起，按你实际的路径导入
from app.models.user import ChatMessage 

# 专门负责往数据库里存聊天记录
def create_chat_message(db: Session, user_id: int, role: str, content: str):
    db_msg = ChatMessage(user_id=user_id, role=role, content=content)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg
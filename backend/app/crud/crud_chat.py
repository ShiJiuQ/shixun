# 具体的增删改查方法
from sqlalchemy.orm import Session
from app.models.chat import ChatSession
from app.schemas.chat import SessionCreate, SessionUpdate
from app.models.chat import ChatMessage
from app.schemas.chat import MessageCreate
# 创建新会话
def create_session(db: Session, session: SessionCreate):
    db_session = ChatSession(user_id=session.user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

# 获取会话列表（支持按标题搜索关键字）
def get_sessions_by_user(db: Session, user_id: int, search_keyword: str = None):
    query = db.query(ChatSession).filter(
        ChatSession.user_id == user_id,
        ChatSession.is_deleted == False  # 只查没被删除的
    )
    
    # 如果前端传了搜索词，就加上模糊查询
    if search_keyword:
        query = query.filter(ChatSession.title.like(f"%{search_keyword}%"))
        
    # 按照置顶和时间倒序排
    return query.order_by(ChatSession.is_pinned.desc(), ChatSession.updated_at.desc()).all()

# 更新会话（改名）
def update_session(db: Session, session_id: int, session_update: SessionUpdate):
    db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if db_session:
        # 如果传了 title 就更新 title
        if session_update.title is not None:
            db_session.title = session_update.title
        # 如果传了 is_pinned 就更新 is_pinned
        if session_update.is_pinned is not None:
            db_session.is_pinned = session_update.is_pinned
            
        db.commit()
        db.refresh(db_session)
    return db_session

# 1. 保存一条新消息 (无论是用户发的，还是AI回复的，都用这个存)
def create_message(db: Session, message: MessageCreate):
    db_message = ChatMessage(
        session_id=message.session_id,
        role=message.role,
        message_type=message.message_type,
        content=message.content,
        attachment_url=message.attachment_url
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# 2. 获取某个会话下的所有聊天记录
def get_messages_by_session(db: Session, session_id: int):
    # 按照时间正序排列，保证聊天记录是从上往下的
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
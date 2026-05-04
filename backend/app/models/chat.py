from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey,Integer
from app.db.database import Base 

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="会话ID")
    #user_id = Column(BigInteger, index=True, nullable=False, comment="用户ID")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String(255), default="新对话", comment="会话主题")
    is_pinned = Column(Boolean, default=False, comment="是否置顶")
    is_deleted = Column(Boolean, default=False, comment="是否已删除（逻辑删除）")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="消息ID")
    session_id = Column(BigInteger, ForeignKey("chat_sessions.id"), index=True, nullable=False)
    #session_id = Column(BigInteger, index=True, nullable=False, comment="关联的会话ID")
    role = Column(String(50), nullable=False, comment="角色：user/assistant/system")
    message_type = Column(String(50), default="text", comment="类型：text/image/file")
    content = Column(String(5000), nullable=False, comment="消息内容")
    attachment_url = Column(String(500), nullable=True, comment="附件链接（图片等）")
    created_at = Column(DateTime, server_default=func.now(), comment="发送时间")
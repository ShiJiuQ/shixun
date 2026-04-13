from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# 1. 新增：用户表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) # 账号不能重复
    hashed_password = Column(String)  # 这里存的是加密后的乱码

    # 关系绑定：一个用户拥有多条聊天记录
    messages = relationship("ChatMessage", back_populates="owner")

# 2. 修改：聊天记录表
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)  
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 关系绑定：这条记录属于哪个用户
    owner = relationship("User", back_populates="messages")
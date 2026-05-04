# 前端传给后端的数据需要做检查（比如改名时，必须传新的 title 过来）
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 前端请求创建会话时传的参数 (目前可能只需要知道是谁建的)
class SessionCreate(BaseModel):
    user_id: int # 实际项目中可能直接从Token拿，这里先简化

# 前端请求修改会话时传的参数（改名、置顶等）
class SessionUpdate(BaseModel):
    title: Optional[str] = None
    is_pinned: Optional[bool] = None

# 后端返回给前端的数据格式
class SessionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    is_pinned: bool
    created_at: datetime

    class Config:
        orm_mode = True  # 让 Pydantic 能读懂 SQLAlchemy 的模型

# 前端发消息时传的参数
class MessageCreate(BaseModel):
    session_id: int
    content: str
    role: str = "user"  # 默认是前端用户发消息
    message_type: str = "text"
    attachment_url: Optional[str] = None # 如果发了图片，这里会有链接

# 返回给前端的消息格式
class MessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    message_type: str
    content: str
    attachment_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
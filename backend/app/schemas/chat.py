from pydantic import BaseModel

# 规定前端发消息时必须传什么格式
class ChatRequest(BaseModel):
    message: str
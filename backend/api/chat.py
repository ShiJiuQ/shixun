import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from openai import AsyncOpenAI

from core.config import settings
from database import get_db, SessionLocal
import models
from core.deps import get_current_user

router = APIRouter()
client = AsyncOpenAI(api_key=settings.ZHIPU_API_KEY, base_url=settings.ZHIPU_BASE_URL)

class ChatRequest(BaseModel):
    message: str

# 定义一个统一的后台存库任务
def save_message_task(user_id: int, role: str, content: str):
    db = SessionLocal()
    try:
        msg = models.ChatMessage(role=role, content=content, user_id=user_id)
        db.add(msg)
        db.commit()
    finally:
        db.close()

@router.post("/")
async def chat_endpoint(
    request: ChatRequest, 
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user)
):
    # 用户消息也扔进后台存，不阻塞主流程起步
    background_tasks.add_task(save_message_task, current_user.id, "user", request.message)

    async def generate():
        full_response = ""
        try:
            response = await client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "system", "content": "你是研途Buddy，一个408考研助手。"},
                    {"role": "user", "content": request.message}
                ],
                stream=True
            )
            
            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    # 标准 SSE 格式
                    yield f"data: {content}\n\n"
                    # 【改动 2】强制刷新！让事件循环有机会把字吐出去
                    await asyncio.sleep(0.01) 
            
            # AI 消息存库
            background_tasks.add_task(save_message_task, current_user.id, "assistant", full_response)
            yield f"data: {content}\n\n"

        except Exception as e:
            print(f"Streaming Error: {e}")
            yield f"data: [ERROR] 服务器开小差了\n\n"

    # 添加全套防缓存 Header
    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache, no-transform", 
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no", # 告诉 Nginx/代理商：别攒着，有多少发多少！
        }
    )
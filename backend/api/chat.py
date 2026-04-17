import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from app.core.config import settings
from app.db.database import SessionLocal
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.crud import crud_chat

router = APIRouter()
client = AsyncOpenAI(api_key=settings.ZHIPU_API_KEY, base_url=settings.ZHIPU_BASE_URL)

# 这是后台任务的包裹函数：因为它在后台运行，所以要单独给它分配一个数据库连接窗口(SessionLocal)
def save_message_task(user_id: int, role: str, content: str):
    db = SessionLocal()
    try:
        # 指派库管员去存库
        crud_chat.create_chat_message(db=db, user_id=user_id, role=role, content=content)
    finally:
        db.close()

@router.post("/")
async def chat_endpoint(
    request: ChatRequest, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user) # 严阵以待的门禁保安
):
    # 1. 先把用户的消息扔进后台存库，不耽误马上呼叫大模型
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
                    yield f"data: {content}\n\n"
                    # 强制刷新缓冲区，产生打字机效果
                    await asyncio.sleep(0.01) 
            
            # 2. 大模型说完了，把 AI 的完整回复也扔进后台存库
            background_tasks.add_task(save_message_task, current_user.id, "assistant", full_response)
            
            # 🚨 核心修复：流式输出结束的标准标识，告诉前端“我说完了”
            yield "data: [DONE]\n\n"

        except Exception as e:
            print(f"Streaming Error: {e}")
            yield f"data: [ERROR] 服务器开小差了\n\n"

    # 返回流式响应，并附带全套防缓存护甲
    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache, no-transform", 
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from openai import AsyncOpenAI

# 确保这些导入路径符合你的项目结构
from app.db.database import get_db, SessionLocal 
from app.schemas import chat as chat_schemas
from app.crud import crud_chat
from app.core.config import settings
import os
from utils.file_parser import FileProcessor
import re
file_processor = FileProcessor(is_multimodal=False)

def extract_and_clean_files(text: str):
    """
    从前端传来的 Markdown 文本中提取本地文件路径，
    并把这些生硬的 URL 从文本中删掉（防止干扰大模型）。
    """
    # 匹配 ![xxx](url) 或 [xxx](url)
    pattern = r'!?\[.*?\]\((.*?)\)'
    urls = re.findall(pattern, text)
    
    local_paths = []
    clean_text = text
    
    for url in urls:
        if "uploads/" in url:
            # 提取出 uploads/ 后面的文件名，拼成本地路径
            file_name = url.split("uploads/")[-1]
            local_path = f"uploads/{file_name}"
            
            if os.path.exists(local_path):
                local_paths.append(local_path)
            
            # 把这段冗长的 url 从发给大模型的文本里抹掉
            clean_text = clean_text.replace(url, "")
            
    # 清理掉残留的 []() 符号
    clean_text = re.sub(r'!?\[.*?\]\(\)', '', clean_text).strip()
    
    return local_paths, clean_text

router = APIRouter()

# 初始化智谱客户端
client = AsyncOpenAI(api_key=settings.ZHIPU_API_KEY, base_url=settings.ZHIPU_BASE_URL)

# ==========================================
# 后台保存消息的任务（赋予独立数据库连接）
# ==========================================
def save_message_task(session_id: int, role: str, content: str):
    """
    后台任务：分配独立的数据库连接窗口，将消息存入对应 session
    """
    db = SessionLocal()
    try:
        msg_data = chat_schemas.MessageCreate(
            session_id=session_id,
            content=content,
            role=role,
            message_type="text"
        )
        crud_chat.create_message(db=db, message=msg_data)
    except Exception as e:
        print(f"后台保存消息失败: {e}")
    finally:
        db.close()


# ==========================================
# 基础 CRUD 接口 (会话管理)
# ==========================================
@router.post("/sessions", response_model=chat_schemas.SessionResponse)
def create_chat_session(session: chat_schemas.SessionCreate, db: Session = Depends(get_db)):
    """新建会话接口"""
    return crud_chat.create_session(db=db, session=session)

@router.get("/sessions", response_model=List[chat_schemas.SessionResponse])
def get_chat_sessions(user_id: int, keyword: str = None, db: Session = Depends(get_db)):
    """获取会话列表及搜索接口"""
    return crud_chat.get_sessions_by_user(db=db, user_id=user_id, search_keyword=keyword)

@router.put("/sessions/{session_id}", response_model=chat_schemas.SessionResponse)
def update_chat_session(session_id: int, session_update: chat_schemas.SessionUpdate, db: Session = Depends(get_db)):
    """修改会话（改名/置顶）接口"""
    updated_session = crud_chat.update_session(db=db, session_id=session_id, session_update=session_update)
    if not updated_session:
        raise HTTPException(status_code=404, detail="会话没找到")
    return updated_session

@router.get("/sessions/{session_id}/messages", response_model=List[chat_schemas.MessageResponse])
def get_chat_history(session_id: int, db: Session = Depends(get_db)):
    """获取某个对话的历史记录"""
    return crud_chat.get_messages_by_session(db=db, session_id=session_id)

# ==========================================
# 核心流式对话接口 (接入智谱、上下文记忆与文件解析)
# ==========================================
@router.post("/messages")
async def send_message_stream(
    message: chat_schemas.MessageCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    发送消息并获取 AI 的流式回复 (带历史记忆和文件智能解析)
    """
    # 魔法拦截：提取文件路径，清洗用户文本
    file_paths, clean_text = extract_and_clean_files(message.content)
    
    # 组装发给大模型的当前内容
    # 现阶段是纯文本模型，所以把所有文件解析出的文字，全拼到一句话里
    final_user_content = clean_text
    for path in file_paths:
        file_data_list = file_processor.process_file(path)
        if file_data_list:
            for data in file_data_list:
                if data["type"] == "text":
                    final_user_content += data["text"]
                # (未来：如果你切到了 glm-4v，这里可以改成拼装 list)

    if not final_user_content.strip():
        final_user_content = "请查看附件并回答"

    # 3. 查询当前会话的历史记录，赋予 AI 记忆
    history_messages = crud_chat.get_messages_by_session(db=db, session_id=message.session_id)
    
    # 4. 构建发给智谱的消息列表
    ai_messages = [{"role": "system", "content": "你是研途Buddy，一个408考研助手。"}]
    
    # 注入历史记录（限制最近 10 条）
    for h in history_messages[-10:]: 
        ai_messages.append({"role": h.role, "content": h.content})
        
    # 放入本次经过“翻译器”处理过的新问题（AI 视角）
    ai_messages.append({"role": "user", "content": final_user_content})

    # 立即把用户的【原始消息】扔进后台存库（前端视角：保留 Markdown 链接以便渲染），不阻塞
    background_tasks.add_task(save_message_task, message.session_id, "user", message.content)

    # 定义流式生成器
    async def generate():
        full_response = ""
        try:
            response = await client.chat.completions.create(
                model="glm-4-flash", # 这里是你当前的纯文本模型
                messages=ai_messages,  # 包含了历史记忆和刚刚解析的文件文本
                stream=True
            )
            
            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    yield f"data: {content}\n\n"
                    # 强制刷新缓冲区，产生平滑的打字机效果
                    await asyncio.sleep(0.01) 
            
            # AI 回复完毕后，将其完整内容交给后台任务存入数据库
            background_tasks.add_task(save_message_task, message.session_id, "assistant", full_response)
            
            # 必须发送结束标识，让前端知道流结束了
            yield "data: [DONE]\n\n"

        except Exception as e:
            print(f"Streaming Error: {e}")
            yield f"data: [ERROR] 服务器开小差了，请稍后再试\n\n"

    # 返回流式响应，附带防缓存护甲
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
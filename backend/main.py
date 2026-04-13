from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat, auth 
import models
from database import engine
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 告诉主程序：所有以 /api/chat 开头的请求，都交给 chat.py 去处理
app.include_router(chat.router, prefix="/api/chat", tags=["AI对话模块"])
app.include_router(auth.router, prefix="/api/auth", tags=["用户认证"])
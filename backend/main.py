from fastapi.middleware.cors import CORSMiddleware
from api import chat, auth, profile, plan, emotion
from app.db.database import engine, Base
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import shutil

Base.metadata.create_all(bind=engine)
app = FastAPI()

# 自动创建一个存放文件的 uploads 文件夹，并挂载为静态目录
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


#  新增上传接口
@app.post("/api/chat/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 将文件保存到 uploads 目录下
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        # 返回可以在浏览器中直接访问的 URL
        file_url = f"http://127.0.0.1:8000/{file_location}"
        return {"url": file_url, "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}


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
app.include_router(profile.router, prefix="/api/profile", tags=["个人画像模块"])
app.include_router(plan.router, prefix="/api/plan", tags=["学习计划模块"])
app.include_router(emotion.router, prefix="/api/emotion", tags=["情绪疗愈模块"])
from core.exam_system.api import exam
from backend.core.exam_system.api import wrong

app.include_router(
    exam.router,
    prefix="/api/exam",
    tags=["真题模块"]
)

app.include_router(
    wrong.router,
    prefix="/api/exam",
    tags=["真题模块"]
)

app.mount("/images", StaticFiles(directory="images"), name="images")
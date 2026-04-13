from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime
import jwt
from fastapi.security import OAuth2PasswordRequestForm

import models
from database import get_db
from core.security import get_password_hash, verify_password

router = APIRouter()

# 定义前端传过来的数据格式（账号 + 密码）
class UserRequest(BaseModel):
    username: str
    password: str

# 签名秘钥（真实项目中这个必须放在 .env 里，现在为了测试先写死）
SECRET_KEY = "yantu_super_secret_key"

@router.post("/register")
def register(user: UserRequest, db: Session = Depends(get_db)):
    # 1. 查重：去数据库找找这个账号有没有被注册过
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="该账号已被注册！")
    
    # 2. 加密：把明文密码变成哈希乱码
    hashed_pw = get_password_hash(user.password)
    
    # 3. 落库：存入数据库
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    
    return {"msg": "注册成功，欢迎加入研途 Buddy！"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="账号或密码错误！")


    expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    token = jwt.encode({"sub": db_user.username, "exp": expire}, SECRET_KEY, algorithm="HS256")
    
    return {"access_token": token, "token_type": "bearer"} # 标准 OAuth2 格式不需要 msg 字段
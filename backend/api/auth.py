import datetime
import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud import crud_user 
from app.db.database import get_db
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password
from app.core.config import settings

router = APIRouter()

# 注意这里的 response_model=UserResponse，安检员会自动把密码拦截掉不返回给前端！
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. 让库管员去查有没有重名
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="该账号已被注册！")
    
    # 2. 让库管员去建新用户
    new_user = crud_user.create_user(db=db, user=user)
    
    return new_user # 直接返回对象，Pydantic 会自动把它转成安全的 JSON

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="账号或密码错误！")
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    token = jwt.encode(
        {"sub": db_user.username, "exp": expire}, 
        settings.SECRET_KEY, 
        algorithm="HS256"
    )
    
    return {"access_token": token, "token_type": "bearer"}
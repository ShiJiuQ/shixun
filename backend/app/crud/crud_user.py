from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

# 1. 查：通过账号找用户
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# 2. 增：把新用户存进数据库
def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password) # 加密
    db_user = User(username=user.username, password=hashed_pw)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # 刷新一下，获取数据库自动生成的 ID
    
    return db_user
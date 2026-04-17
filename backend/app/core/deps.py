from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.core.config import settings

# 使用绝对路径导入数据库引擎
from app.db.database import get_db
# 引入我们专门负责用户表增删改查的“库管员”
from app.crud import crud_user 
# 告诉 FastAPI，前端应该从哪个接口去获取 Token（用于自动生成文档）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# 这就是我们的“铁面保安”函数
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # 1. 验真伪：尝试解密这张通行证
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的通行证")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="通行证已过期或被篡改，请重新登录")
    
    # 👇 3. 查户口：告别丑陋的 db.query，直接呼叫库管员！
    user = crud_user.get_user_by_username(db, username=username)
    
    if user is None:
        raise HTTPException(status_code=401, detail="找不到该用户")
    
    # 如果一切都没问题，把这个用户的完整信息放行
    return user
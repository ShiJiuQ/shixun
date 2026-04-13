from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from database import get_db
import models

# 告诉 FastAPI，前端应该从哪个接口去获取 Token（用于自动生成文档）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# 这里必须和 auth.py 里的秘钥保持绝对一致！
SECRET_KEY = "yantu_super_secret_key"

# 这就是我们的“铁面保安”函数
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # 1. 验真伪：尝试解密这张通行证
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的通行证")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="通行证已过期或被篡改，请重新登录")
    
    # 2. 查户口：去数据库里确认这个用户是不是真的存在
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="找不到该用户")
    
    # 如果一切都没问题，把这个用户的完整信息放行
    return user
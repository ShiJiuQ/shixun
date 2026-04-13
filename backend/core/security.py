# backend/core/security.py
from passlib.context import CryptContext

# 告诉系统，我们采用极其安全的 bcrypt 算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 把用户输入的明文密码，变成哈希乱码（注册时用）
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 验证密码是否正确（登录时用）
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
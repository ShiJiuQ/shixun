from pydantic import BaseModel

# 1. 前端发过来的注册/登录数据
class UserCreate(BaseModel):
    username: str
    password: str

# 2. 返回给前端的用户信息（安全脱敏版）
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True # 允许 Pydantic 自动读取数据库模型
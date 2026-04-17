from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. 检查配置是否成功读取
if not settings.DATABASE_URL:
    raise ValueError("数据库连接地址未找到，请检查 .env 文件！")

# 2. 创建 MySQL 引擎 (pool_pre_ping 保证连接不会因为闲置而断开)
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 3. 创建 Session 工厂 (每次请求时分配一个数据库连接)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建所有数据表的父类
Base = declarative_base()

# 5. 依赖注入函数：供 api 路由调用，用完自动关闭连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
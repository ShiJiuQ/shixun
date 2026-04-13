from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库文件就叫 yantu.db，会自动生成在 backend 目录下
SQLALCHEMY_DATABASE_URL = "sqlite:///./yantu.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 获取数据库连接的工具函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
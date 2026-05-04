from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from app.db.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(String(50))
    question_id = Column(String(50))

    is_correct = Column(Boolean)
    score = Column(Integer)

    mode = Column(String(20))          # exam / practice
    paper_id = Column(String(20))      # 年份

    knowledge_point = Column(String(255))

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )
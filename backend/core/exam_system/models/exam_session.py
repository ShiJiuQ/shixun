from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


#套卷时间记录
class ExamSession(Base):
    __tablename__ = "exam_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50))
    paper_id = Column(String(20))

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    duration = Column(Integer)
    status = Column(String(20))

    total_score = Column(Integer)
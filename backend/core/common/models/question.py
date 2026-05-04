from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.mysql import JSON
from app.db.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(10), primary_key=True)
    exam_year = Column(Integer)
    question_no = Column(Integer)

    question_type = Column(String(20))
    subject_name = Column(String(50))

    question_content = Column(Text)

    options = Column(JSON)
    standard_answer = Column(String(10))

    analysis_content = Column(Text)

    source_url = Column(Text)
    question_source = Column(String(20))

    knowledge_point = Column(String(100))

    images = Column(JSON)
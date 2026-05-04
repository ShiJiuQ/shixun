import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import declarative_base

# ⚠️ 改成你自己的数据库密码
DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/yantu_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Question(Base):
    __tablename__ = ("questions")

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


# 读取 JSON
with open("408.json", "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0

for item in data:
    q = Question(
        id=item["id"],
        exam_year=item["exam_year"],
        question_no=item["question_no"],
        question_type=item["question_type"],
        subject_name=item["subject_name"],
        question_content=item["question_content"],
        options=item["options"],
        standard_answer=item["standard_answer"],
        analysis_content=item["analysis_content"],
        source_url=item["source_url"],
        question_source=item["question_source"],
        knowledge_point=item.get("knowledge_point", ""),
        images=item.get("images", [])
    )

    session.merge(q)
    count += 1

session.commit()

print(f"✅ 成功导入 {count} 条数据")
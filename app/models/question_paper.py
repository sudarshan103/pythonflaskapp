from sqlalchemy import Column, SmallInteger, String
from app import db

class QuestionPaper(db.Model):
    __tablename__ = 'question_paper'  # Name of the table in the database
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    subject = Column(String(256), nullable=False)
    chapter = Column(String(256), default=None)
    question = Column(String(500), nullable=False)
    options = Column(String(500), nullable=True)
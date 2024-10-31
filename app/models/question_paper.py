from typing import List

from sqlalchemy import Column, SmallInteger, String, Boolean
from app import db

class QuestionPaper(db.Model):
    __tablename__ = 'question_paper'  # Name of the table in the database
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    subject = Column(String(256), nullable=True)
    chapter = Column(String(256), nullable=True)
    question = Column(String(500), nullable=False)
    options = Column(String(500), nullable=True)
    is_multi_choice = Column(Boolean, nullable=False, default=False)

class Question:
    def __init__(self, question_text: str):
        self.question_text = question_text

class ObjectiveQuestion(Question):
    def __init__(self, question_text: str, options: str, multi_choice:bool):
        super().__init__(question_text)
        self.options = options
        self.multi_choice = multi_choice
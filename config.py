import os


class Config:
    SECRET_KEY = 'supersecretkey'
    OUTPUT_FOLDER = 'content'
    QUESTION_FORMAT = r"\d+\.\s(?:.*\n)*?.*?\?"
    DB_CREDENTIALS= os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
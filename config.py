import os

from dotenv import load_dotenv

load_dotenv('env_config/local.env')

class Config:
    SECRET_KEY = 'supersecretkey'
    OUTPUT_FOLDER = 'content'
    QUESTION_FORMAT = r"\d+\.\s(?:.*\n)*?.*?\?"
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
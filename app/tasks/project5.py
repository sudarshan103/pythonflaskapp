import glob
import os
import re
import sys
import PyPDF2

from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError

from app import app, db
from app.models.question_paper_repository import QuestionPaperRepo

def check_database_status(table_name) -> bool :
    with app.app_context():
        try:
            db.session.execute(text("select 1"))
            # Check if table exists
            inspector = inspect(db.engine)
            if table_name in inspector.get_table_names():
                return True
            else:
                print(f"Table '{table_name}' does not exist in the database.")
                return False
        except OperationalError as e:
            return False

def write_db(chapter_name:str = None):
    folder_three = "content/Three"
    if not os.path.exists(folder_three):
        os.makedirs(folder_three)
        print("Pdf file is not present in the folder")
    else:
        pdf_files = []
        pdf_files.extend(glob.glob(os.path.join(folder_three, '**', '*.pdf'), recursive=True))
        if len(pdf_files) > 0:
            if validate_input(pdf_files[0],chapter_name):
                pdf_to_db(pdf_files[0])
            else:
                print("Chapter name not found")
        else:
            print("Pdf file is not present in the folder")

def validate_input(pdf_path, chapter_name):
    pdf_text = ""
    if chapter_name is None:
        return True
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page_num].extract_text()
            return chapter_name.lower() in pdf_text.lower()
    except FileNotFoundError:
        print("The PDF file was not found.")
    except Exception as e:
        print("An error occurred:", e)
    return False

def pdf_to_db(pdf_path, chapter_name = None):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            content_text = ""
            last_known_chapter = ""
            paper = []
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page_num in range(len(pdf_reader.pages)):
                text = pdf_reader.pages[page_num].extract_text()
                if text:
                    content_text += text
                    questions = re.findall(app.config['QUESTION_FORMAT'], text, re.MULTILINE)
                    chapter_text = re.findall(r"(Chapter.*?)(?=\s*1\.)", text, re.DOTALL)
                    if chapter_text:
                        last_known_chapter = re.sub(r"\n", " ", chapter_text[0])
                    for question in questions:
                        answer_text = ""
                        clean_question = re.sub(r"\n", " ", question)
                        escaped_ques = re.escape(question)
                        answers = re.findall(rf"{escaped_ques}([\s\S]*?)(?=\s*Answer:)", text, re.DOTALL)
                        for answer in answers:
                            answer_text += re.sub(r"\n", " ", answer)

                        if answers:
                            paper.append(dict(subject="Chemistry",
                                              chapter=last_known_chapter,
                                              question = clean_question,
                                              options = answer_text
                                              )
                                         )

            if len(paper) > 0:
                with app.app_context():
                    QuestionPaperRepo.bulk_create(paper)
    except FileNotFoundError:
        print("The PDF file was not found.")
    except Exception as e:
        print("An error occurred:", e)

def process_input(chapter_name:str = None):
    if check_database_status("question_paper"):
        write_db(chapter_name)
    else:
        print("Database is not available or question_paper table is missing")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            sanitized_user_input = sys.argv[1]
            process_input(sanitized_user_input)
        except ValueError:
            print("Please enter chapter name in double quotes")
    else:
        process_input()

# export PYTHONPATH=$(pwd)
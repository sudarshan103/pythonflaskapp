import glob
import os
import re
import sys
import PyPDF2

from app import app
from app.models.question_paper_repository import QuestionPaperRepo
from app.utils.utils import check_database_status

def write_db():
    folder_three = "content/Three"
    if not os.path.exists(folder_three):
        os.makedirs(folder_three)
        print("Pdf file is not present in the folder")
    else:
        pdf_files = []
        pdf_files.extend(glob.glob(os.path.join(folder_three, '**', '*.pdf'), recursive=True))
        if len(pdf_files) > 0:
            pdf_to_db(pdf_files[0])
        else:
            print("Pdf file is not present in the folder")

def pdf_to_db(pdf_path):
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
                    chapter_text = re.findall(app.config['CHAPTER_TITLE_FORMAT'], text, re.DOTALL)
                    if chapter_text:
                        last_known_chapter = re.sub(r"\n", " ", chapter_text[0])
                    for question in questions:
                        answer_text = ""
                        clean_question = re.sub(r"\n", " ", question)
                        escaped_ques = re.escape(question)
                        answers = re.findall(rf"{escaped_ques}{app.config['ANSWER_FORMAT']}", text, re.DOTALL)
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

def process_input():
    if check_database_status("question_paper"):
        write_db()
    else:
        print("Database is not available or question_paper table is missing")

if __name__ == "__main__":
    process_input()


# export PYTHONPATH=$(pwd)
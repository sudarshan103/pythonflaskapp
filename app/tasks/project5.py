import glob
import os
import re
import sys
import PyPDF2
from sqlalchemy.testing.plugin.plugin_base import options

from app import app
from app.models.question_paper_repository import QuestionPaperRepo


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
            ques = []
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                text = pdf_reader.pages[page_num].extract_text()
                if text:
                    questions = re.findall(app.config['QUESTION_FORMAT'], text, re.MULTILINE)
                    for question in questions:
                        clean_question = re.sub(r"\n", " ", question)
                        ques.append(dict(subject = "Chemistry", chapter = "Any", question = clean_question, options = "{}"))
            if len(ques) > 0:
                QuestionPaperRepo.bulk_create(ques)
    except FileNotFoundError:
        print("The PDF file was not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            sanitized_user_input = sys.argv[1]
            write_db(sanitized_user_input)
        except ValueError:
            print("Please enter chapter name in double quotes")
    else:
        write_db()

# export PYTHONPATH=$(pwd)
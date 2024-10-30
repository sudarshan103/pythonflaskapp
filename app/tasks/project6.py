import os
import sys

from app import app
from app.models.question_paper_repository import QuestionPaperRepo
from app.utils.app_utils import check_database_status
from app.utils.utils import contains_sql_injection_chars


def print_questions(chapter_name:str):
    folder_three = "content/Three"
    if not os.path.exists(folder_three):
        os.makedirs(folder_three)
        print("Pdf file is not present in the folder")
    else:
        questions = ""
        with app.app_context():
            result = QuestionPaperRepo.get_by_chapter(chapter_name)
            if result:
                for row in result:
                    questions += f"{row.question}\n"
            else:
                questions += "No questions found"

            print(questions)

def process_input(chapter_name:str):
    if check_database_status("question_paper"):
        print_questions(chapter_name)
    else:
        print("Database is not available or question_paper table is missing")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            user_input = sys.argv[1].strip()
            if not user_input:
                print("Please enter chapter name in double quotes")
            elif contains_sql_injection_chars(user_input):
                print("Input has restricted characters")
            else:
                process_input(user_input)
        except ValueError:
            print("Please enter chapter name in double quotes")
    else:
        print("Please enter chapter name in double quotes")

# export PYTHONPATH=$(pwd)
import glob
import os
import re
import sys

from app import app
from app.utils.utils import validate_page_input, extract_text_from_pdf


def write_file(page_number:int):
    folder_three = "content/Three"
    if not os.path.exists(folder_three):
        os.makedirs(folder_three)
        print("Pdf file is not present in the folder")
    else:
        pdf_files = []
        pdf_files.extend(glob.glob(os.path.join(folder_three, '**', '*.pdf'), recursive=True))
        txt_filename = 'output.txt'
        if len(pdf_files) > 0:
            if validate_page_input(pdf_files[0],page_number):
                pdf_text = extract_text_from_pdf(pdf_files[0],page_number)
                question_text = ""
                questions = re.findall(app.config['QUESTION_FORMAT'], pdf_text, re.MULTILINE)
                for question in questions:
                    clean_question = re.sub(r"\n", " ", question)
                    question_text += f"{clean_question}\n"
                txt_file_path = os.path.join(folder_three, txt_filename)
                with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(question_text)
                print("Written page into txt")
        else:
            print("Pdf file is not present in the folder")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            user_input = int(sys.argv[1])
            write_file(user_input-1)
        except ValueError:
            print("Please enter a page number along with command.")
    else:
        print("Please enter a page number along with command.")

# export PYTHONPATH=$(pwd)
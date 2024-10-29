import glob
import os
import re
import sys
import PyPDF2

from app import app


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
                txt_file_path = os.path.join(folder_three, txt_filename)
                with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(pdf_text)
                print("Written page into txt")
        else:
            print("Pdf file is not present in the folder")

def validate_page_input(pdf_path, page_number):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            if page_number < 0 or page_number >= len(pdf_reader.pages):
                print(f"Page {page_number+1} does not exist.")
                return False
    except FileNotFoundError:
        print("The PDF file was not found.")
    except Exception as e:
        print("An error occurred:", e)
    return True

def extract_text_from_pdf(pdf_path, page_number):
    question_text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page = pdf_reader.pages[page_number]
            text = page.extract_text()
            if text:
                question_text = ""
                questions = re.findall(app.config['QUESTION_FORMAT'], text, re.MULTILINE)
                for question in questions:
                    clean_question = re.sub(r"\n", " ", question)
                    question_text += f"{clean_question}\n"
            else:
                print("No text found on the specified page.")
    except FileNotFoundError:
        print("The PDF file was not found.")
    except Exception as e:
        print("An error occurred:", e)
    return question_text

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
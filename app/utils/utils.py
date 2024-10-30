import os
import re

import PyPDF2
from sqlalchemy import text, inspect
from sqlalchemy.exc import OperationalError

from app.constants import sql_injection_pattern

def print_outcome(outcome:str):
    txt_filename = 'debug_outcome.txt'
    txt_file_path = os.path.join("app", txt_filename)
    if not os.path.exists(txt_file_path):
        os.makedirs(txt_file_path)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(outcome)
    print("Written into debug_outcome")

def contains_sql_injection_chars(input_text: str) -> bool:
    return bool(re.search(sql_injection_pattern, input_text))


def extract_text_from_pdf(pdf_path, page_number=None):
    pdf_text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            if page_number:
                page = pdf_reader.pages[page_number]
                pdf_text = page.extract_text()
                if pdf_text:
                    return pdf_text
                else:
                    print("No text found on the specified page.")
            else:
                for page_num in range(len(pdf_reader.pages)):
                    pdf_text += pdf_reader.pages[page_num].extract_text()
                return pdf_text
            return None
    except FileNotFoundError:
        print("The PDF file was not found.")
    except Exception as e:
        print("An error occurred:", e)

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
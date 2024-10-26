import glob
import os

from PyPDF2 import PdfReader
from flask import render_template, request, redirect, url_for, flash, current_app


def collect_content():
    content_folder =  current_app.config['OUTPUT_FOLDER']
    folder_one = f"{current_app.config['OUTPUT_FOLDER']}/One"
    folder_two = f"{current_app.config['OUTPUT_FOLDER']}/Two"
    folder_three = f"{current_app.config['OUTPUT_FOLDER']}/Three"

    if not os.path.exists(content_folder):
        os.makedirs(content_folder)
    if not os.path.exists(folder_one):
        os.makedirs(folder_one)
    if not os.path.exists(folder_two):
        os.makedirs(folder_two)
    if not os.path.exists(folder_three):
        os.makedirs(folder_three)

    if request.method == 'GET':
        pdf_files = []
        pdf_files.extend(glob.glob(os.path.join(content_folder, '**', '*.pdf'), recursive=True))
        txt_filename = 'output.txt'
        for pdf in pdf_files:
            pdf_text = extract_text_from_pdf(pdf)
            txt_file_path = os.path.join(os.path.dirname(pdf), txt_filename)
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(pdf_text)
            flash(f'PDF file "{pdf}" processed and saved as "{txt_filename}"!')

    return render_template('output.html')

def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            pdf_text += reader.pages[page_num].extract_text()
    return pdf_text
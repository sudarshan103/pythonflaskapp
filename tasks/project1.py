import os

from PyPDF2 import PdfReader
from flask import render_template, request, redirect, url_for, flash

from app import app

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    # Ensure the uploads directory exists
    if not os.path.exists(app.config['OUTPUT_FOLDER'] ):
        os.makedirs(app.config['OUTPUT_FOLDER'] )

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select a file, browser may submit an empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Save the file if it's allowed
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            file.save(file_path)
            flash(f'File "{filename}" successfully uploaded!')
            pdf_text = extract_text_from_pdf(file_path)

            # Write the extracted text to a .txt file
            txt_filename = 'output.txt'
            txt_file_path = os.path.join(app.config['OUTPUT_FOLDER'], txt_filename)
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(pdf_text)
            flash(f'PDF file "{filename}" processed and saved as "{txt_filename}"!')
            return redirect(url_for('uploaded_file', filename=txt_filename))

    return render_template('index.html')

def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            pdf_text += reader.pages[page_num].extract_text()
    return pdf_text
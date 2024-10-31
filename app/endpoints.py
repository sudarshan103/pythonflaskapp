import os

from flask import Blueprint, send_from_directory, render_template, flash, current_app, Response

from app.tasks import project1, project2

# Initialize the Blueprint
endpoints = Blueprint('endpoints', __name__)

# Define the root route
@endpoints.route('/', methods=['GET'])
def home():
    flash('Welcome to Flask with Python!')
    return render_template('output.html')

@endpoints.route('/project1', methods=['GET'])
def project_one():
    flash('Upload a file')
    return render_template('index.html')

# Define upload route
@endpoints.route('/project1', methods=['POST'])
def upload_file():
    return project1.upload_file()

# Route to serve files from the content folder
@endpoints.route('/content/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(current_app.config['OUTPUT_FOLDER'], filename)
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return Response(content, mimetype='text/plain')
    except FileNotFoundError:
        return "File not found", 404

# Route for collect_content functionality
@endpoints.route('/project2')
def project_two():
    return project2.collect_content()
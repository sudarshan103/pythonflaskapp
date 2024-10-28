from flask import Blueprint, send_from_directory, render_template, flash, current_app

from app.tasks import project1, project2

# Initialize the Blueprint
endpoints = Blueprint('endpoints', __name__)

# Define the root route
@endpoints.route('/', methods=['GET'])
def home():
    flash('Welcome to Flask with Python!')
    return render_template('output.html')

# Define upload route
@endpoints.route('/upload', methods=['POST'])
def upload_file():
    return project1.upload_file()

# Route to serve files from the content folder
@endpoints.route('/content/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['OUTPUT_FOLDER'], filename)

# Route for collect_content functionality
@endpoints.route('/content/collect')
def collect_content():
    return project2.collect_content()
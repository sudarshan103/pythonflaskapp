import os
from flask import Flask, send_from_directory
from tasks import project1

# Initialize the Flask app
app = Flask(__name__)

# Secret key for flashing messages
app.config['SECRET_KEY'] = 'supersecretkey'

# Folder where uploaded files will be stored
app.config['OUTPUT_FOLDER'] = 'content'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
   return project1.upload_file()

@app.route('/content/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

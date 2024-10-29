from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
from app.endpoints import endpoints

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(endpoints)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

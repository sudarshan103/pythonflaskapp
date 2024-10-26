from flask import Flask

from config import Config
from endpoints import endpoints

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(endpoints)

if __name__ == '__main__':
    app.run(debug=True)

# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# config.py
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import the views and models modules
from . import views, models

# Create the Flask app
app = Flask(__name__)

# Load the app settings from config.py
app.config.from_object("config")

# Create the database object
db = SQLAlchemy(app)

# Run the app if this file is executed
if __name__ == "__main__":
    app.run()


# Set the database URI
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///data.db"

# Set the secret key
SECRET_KEY = os.environ.get("SECRET_KEY") or "some-random-string"

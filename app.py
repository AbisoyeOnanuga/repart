# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app
app = Flask(__name__)

# Load the app settings from config.py
app.config.from_object("config")

# Create the database object
db = SQLAlchemy(app)

# Import the views and models modules
from . import views, models

# Run the app if this file is executed
if __name__ == "__main__":
    app.run()

# config.py
import os

# Set the database URI
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///data.db"

# Set the secret key
SECRET_KEY = os.environ.get("SECRET_KEY") or "some-random-string"

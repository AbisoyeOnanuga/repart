# config.py
import os

# Set the database URI
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///data.db"

# Set the secret key
SECRET_KEY = os.environ.get("SECRET_KEY") or "some-random-string"

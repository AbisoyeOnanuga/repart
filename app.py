# app.py
# Import Flask and other modules
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
import os

# Import RavenDB and Gravitee
from ravendb import DocumentStore
from gravitee import Gravitee

# Define the Item class
class Item:
    def __init__(self, id, name, price, location, description, category, user_id, lon, lat, gpuspeed, gpuprocessor):
        self.id = id
        self.name = name
        self.price = price
        self.location = location
        self.lon = lon
        self.lat = lat
        self.description = description
        self.category = category
        self.user_id = user_id
        self.gpuspeed = gpuspeed
        self.gpuprocessor = gpuprocessor

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, price={self.price}, location={self.location}, description={self.description}, category={self.category}, user_id={self.user_id})"

# Define the config module
class Config:
    # Define the secret key for Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret"

    # Define the Google OAuth credentials
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    # Define the RavenDB URL and database name
    RAVENDB_URL = os.environ.get("RAVENDB_URL") or "http://localhost:8080"
    RAVENDB_DATABASE = os.environ.get("RAVENDB_DATABASE") or "repart"

    # Define the Gravitee API key and base URL
    GRAVITEE_API_KEY = os.environ.get("GRAVITEE_API_KEY")
    GRAVITEE_BASE_URL = os.environ.get("GRAVITEE_BASE_URL") or "https://api.gravitee.io"

# Create a Flask app instance
app = Flask(__name__)

# Load the configuration from config.py
app.config.from_object("config")

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the OAuth client
client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])

# Initialize the document store
store = DocumentStore(app.config["RAVENDB_URL"], "RePart")
store.initialize()

# Initialize the Gravitee instance
gravitee = Gravitee(app.config["GRAVITEE_API_KEY"], app.config["GRAVITEE_BASE_URL"])

# Define a user class
class User:
    def __init__(self, id, name, email, profile_pic):
        self.id = id
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, profile_pic={self.profile_pic})"

# Define a login callback function
@login_manager.user_loader
def load_user(user_id):
    # Open a session
    with store.open_session() as session:
        # Query the database for the user by id
        user = session.query(User).where(id=user_id).first()
        # Return the user object
        return user

# Define a route for the home page
@app.route("/")
def home():
    # Open a session
    with store.open_session() as session:
        # Query the database for all items
        items = session.query(Item).all()
        # Render the home template with the items
        return render_template("home.html", items=items)

# Define a route for the item page
@app.route("/items/<int:id>")
def item(id):
    # Open a session
    with store.open_session() as session:
        # Query the database for the item by id
        item = session.query(Item).where(id=id).first()
        # Check if the item exists
        if item:
            # Render the item template with the item
            return render_template("item.html", item=item)
        else:
            # Flash an error message
            flash("Item not found")
            # Redirect to the home page
            return redirect(url_for("home"))

# Define a route for the login page
@app.route("/login")
def login():
    # Check if the user is already logged in
    if current_user.is_authenticated:
        # Redirect to the home page
        return redirect(url_for("home"))
    else:
        # Generate a Google authorization URL
        google_provider_cfg = requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        # Redirect to the Google authorization URL
        return redirect(request_uri)

# Define a route for the login callback
@app.route("/login/callback")
def callback():
    # Get the authorization code from the request
    code = request.args.get("code")
    # Prepare and send a token request to get the access token
    google_provider_cfg = requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config["GOOGLE_CLIENT_ID"], app.config["GOOGLE_CLIENT_SECRET"]),
    )
    # Parse the access token from the response
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Prepare and send a userinfo request to get the user information
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # Parse the user information from the response
    if userinfo_response.json().get("email_verified"):
        user_id = userinfo_response.json()["sub"]
        user_name = userinfo_response.json()["name"]
        user_email = userinfo_response.json()["email"]
        user_profile_pic = userinfo_response.json()["picture"]
    else:
        # Flash an error message
        flash("User email not available or not verified by Google")
        # Redirect to the login page
        return redirect(url_for("login"))
    # Check if the user exists in the database
    with store.open_session() as session:
        user = session.query(User).where(id=user_id).first()
        # If the user does not exist, create a new user and save it to the database
        if not user:
            user = User(id=user_id, name=user_name, email=user_email, profile_pic=user_profile_pic)
            session.store(user)
            session.save_changes()
    # Log the user in
    login_user(user)
    # Flash a success message
    flash("You have successfully logged in")
    # Redirect to the home page
    return redirect(url_for("home"))

# Define a route for the logout page
@app.route("/logout")
@login_required
def logout():
    # Log the user out
    logout_user()
    # Flash a success message
    flash("You have successfully logged out")
    # Redirect to the home page
    return redirect(url_for("home"))

# Define a route for the create page
@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    # Check if the request method is POST
    if request.method == "POST":
        # Get the form data from the request
        name = request.form.get("name")
        price = request.form.get("price")
        location = request.form.get("location")
        description = request.form.get("description")
        category = request.form.get("category")
        # Validate the form data
        if not name or not price or not location or not description or not category:
            # Flash an error message
            flash("Please fill in all the fields")
            # Redirect to the create page
            return redirect(url_for("create"))
        else:
            # Create a new item object
            item = Item(name=name, price=price, location=location, description=description, category=category, user_id=current_user.id)
            # Open a session
            with store.open_session() as session:
                # Save the item to the database
                session.store(item)
                session.save_changes()
            # Flash a success message
            flash("Item created successfully")
            # Redirect to the item page
            return redirect(url_for("item", id=item.id))
    else:
        # Render the create template
        return render_template("create.html")

# Define a route for the edit page
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    # Open a session
    with store.open_session() as session:
        # Query the database for the item by id
        item = session.query(Item).where(id=id).first()
        # Check if the item exists
        if item:
            # Check if the current user is the owner of the item
            if current_user.id == item.user_id:
                # Check if the request method is POST
                if request.method == "POST":
                    # Get the form data from the request
                    name = request.form.get("name")
                    price = request.form.get("price")
                    location = request.form.get("location")
                    description = request.form.get("description")
                    category = request.form.get("category")
                    # Validate the form data
                    if not name or not price or not location or not description or not category:
                        # Flash an error message
                        flash("Please fill in all the fields")
                        # Redirect to the edit page
                        return redirect(url_for("edit", id=id))
                    else:
                        # Update the item attributes
                        item.name = name
                        item.price = price
                        item.location = location
                        item.description = description
                        item.category = category
                        # Save the changes to the database
                        session.save_changes()
                        # Flash a success message
                        flash("Item updated successfully")
                        # Redirect to the item page
                        return redirect(url_for("item", id=id))
                else:
                    # Render the edit template with the item
                    return render_template("edit.html", item=item)
            else:
                # Flash an error message
                flash("You are not authorized to edit this item")
                # Redirect to the home page
                return redirect(url_for("home"))
        else:
            # Flash an error message
            flash("Item not found")
            # Redirect to the home page
            return redirect(url_for("home"))

# Define a route for the delete page
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    # Open a session
    with store.open_session() as session:
        # Query the database for the item by id
        item = session.query(Item).where(id=id).first()
        # Check if the item exists
        if item:
            # Check if the current user is the owner of the item
            if current_user.id == item.user_id:
                # Delete the item from the database
                session.delete(item)
                session.save_changes()
                # Flash a success message
                flash("Item deleted successfully")
                # Redirect to the home page
                return redirect(url_for("home"))
            else:
                # Flash an error message
                flash("You are not authorized to delete this item")
                # Redirect to the home page
                return redirect(url_for("home"))
        else:
            # Flash an error message
            flash("Item not found")
            # Redirect to the home page
            return redirect(url_for("home"))
# website/urls.py
from flask import Blueprint
from ..app import views

# Create a blueprint for the website app
website = Blueprint("website", __name__)

# Define the URL rules for the website app
website.add_url_rule("/", view_func=views.home, methods=["GET"], endpoint="home")
website.add_url_rule("/product/<int:id>/", view_func=views.product_detail, methods=["GET"], endpoint="product_detail")
website.add_url_rule("/cart/", view_func=views.cart, methods=["GET"], endpoint="cart")
website.add_url_rule("/checkout/", view_func=views.checkout, methods=["GET", "POST"], endpoint="checkout")
website.add_url_rule("/login/", view_func=views.login, methods=["GET", "POST"], endpoint="login")
website.add_url_rule("/register/", view_func=views.register, methods=["GET", "POST"], endpoint="register")
website.add_url_rule("/logout/", view_func=views.logout, methods=["GET"], endpoint="logout")
website.add_url_rule("/thank_you/", view_func=views.thank_you, methods=["GET"], endpoint="thank_you")

# views.py
from flask import render_template, request, session, redirect, url_for, flash
from . import app, db
from .models import Product, Customer, Order, OrderItem
from .forms import LoginForm, RegisterForm, CheckoutForm
import uuid # Import the uuid module

# Create your views here.

@app.route("/")
def home():
    # Get all the products from the database
    products = Product.objects.all()
    # Render the home page template with the products
    return render_template("home.html", products=products)

@app.route("/product/<int:id>/")
def product_detail(id):
    # Get the product by its id from the database
    product = Product.objects.get(id=id)
    # Render the product detail page template with the product
    return render_template("product_detail.html", product=product)

@app.route("/cart/")
def cart():
    # Check if the user is logged in
    if "user_id" in session:
        # Get the customer from the session user id
        customer = Customer.objects.get(id=session["user_id"])
        # Get the order by the customer from the database
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Get the order items by the order from the database
        order_items = order.orderitem_set.all()
        # Render the cart page template with the order and order items
        return render_template("cart.html", order=order, order_items=order_items)
    else:
        # Redirect the user to the login page with a message
        flash("Please log in to view your cart.")
        return redirect(url_for("login"))

@app.route("/checkout/", methods=["GET", "POST"])
def checkout():
    # Check if the user is logged in
    if "user_id" in session:
        # Get the customer from the session user id
        customer = Customer.objects.get(id=session["user_id"])
        # Get the order by the customer from the database
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Get the order items by the order from the database
        order_items = order.orderitem_set.all()
        # Create a checkout form
        form = CheckoutForm()
        # Check if the form is submitted and valid
        if form.validate_on_submit():
            # Update the order with the form data
            order.name = form.name.data
            order.email = form.email.data
            order.address = form.address.data
            order.city = form.city.data
            order.state = form.state.data
            order.zip_code = form.zip_code.data
            order.complete = True
            # Generate a random transaction id
            order.transaction_id = str(uuid.uuid4())
            # Save the order to the database
            order.save()
            # Clear the session
            session.clear()
            # Redirect the user to the thank you page with a message
            flash("Thank you for your purchase.")
            return redirect(url_for("thank_you"))
        # Render the checkout page template with the order, order items, and form
        return render_template("checkout.html", order=order, order_items=order_items, form=form)
    else:
        # Redirect the user to the login page with a message
        flash("Please log in to proceed to checkout.")
        return redirect(url_for("login"))

@app.route("/login/", methods=["GET", "POST"])
def login():
    # Check if the user is already logged in
    if "user_id" in session:
        # Redirect the user to the home page
        return redirect(url_for("home"))
    else:
        # Create a login form
        form = LoginForm()
        # Check if the form is submitted and valid
        if form.validate_on_submit():
            # Get the email and password from the form
            email = form.email.data
            password = form.password.data
            # Try to get the customer by the email from the database
            customer = Customer.objects.filter(email=email).first()
            # Check if the customer exists and the password matches
            if customer and customer.password == password:
                # Set the session user id to the customer id
                session["user_id"] = customer.id
                # Redirect the user to the home page with a message
                flash("You have successfully logged in.")
                return redirect(url_for("home"))
            else:
                # Flash an error message
                flash("Invalid email or password.")
        # Render the login page template with the form
        return render_template("login.html", form=form)

@app.route("/register/", methods=["GET", "POST"])
def register():
    # Check if the user is already logged in
    if "user_id" in session:
        # Redirect the user to the home page
        return redirect(url_for("home"))
    else:
        # Create a register form
        form = RegisterForm()
        # Check if the form is submitted and valid
        if form.validate_on_submit():
            # Get the name, email, and password from the form
            name = form.name.data
            email = form.email.data
            password = form.password.data
            # Try to get the customer by the email from the database
            customer = Customer.objects.filter(email=email).first()
            # Check if the customer already exists
            if customer:
                # Flash an error message
                flash("Email already registered.")
            else:
                # Create a new customer with the form data
                customer = Customer(name=name, email=email, password=password)
                # Save the customer to the database
                customer.save()
                # Set the session user id to the customer id
                session["user_id"] = customer.id
                # Redirect the user to the home page with a message
                flash("You have successfully registered.")
                return redirect(url_for("home"))
        # Render the register page template with the form
        return render_template("register.html", form=form)

@app.route("/logout/")
def logout():
    # Check if the user is logged in
    if "user_id" in session:
        # Clear the session
        session.clear()
        # Redirect the user to the home page with a message
        flash("You have successfully logged out.")
        return redirect(url_for("home"))
    else:
        # Redirect the user to the home page
        return redirect(url_for("home"))

@app.route("/thank_you/")
def thank_you():
    # Render the thank you page template
    return render_template("thank_you.html")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DecimalField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# Create your forms here.

class LoginForm(FlaskForm):
    # A login form with email and password fields
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    # A register form with name, email, password, and confirm password fields
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class CheckoutForm(FlaskForm):
    # A checkout form with name, email, address, city, state, zip code, and payment fields
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[DataRequired(), Length(max=200)])
    city = StringField("City", validators=[DataRequired(), Length(max=100)])
    state = StringField("State", validators=[DataRequired(), Length(max=100)])
    zip_code = StringField("Zip Code", validators=[DataRequired(), Length(max=10)])
    payment = RadioField("Payment", choices=[("credit", "Credit Card"), ("paypal", "PayPal"), ("donate", "Donate")], validators=[DataRequired()])
    submit = SubmitField("Checkout")
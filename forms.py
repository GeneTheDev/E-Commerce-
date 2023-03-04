from flask_wtf import FlaskForm
from wtforms import StringField, FloatField


class RegisterForm(FlaskForm):
    """Register User """

    first_name = StringField("First Name")

    last_name = StringField("Last Name")

    username = StringField("Username")

    email = StringField("Email")

    address = StringField("Address")

    password = StringField("Password")


class LoginForm(FlaskForm):
    """Login User"""

    username = StringField("Username")

    password = StringField("Password")

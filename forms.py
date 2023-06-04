from flask_wtf import FlaskForm
from wtforms.validators import Email
from wtforms import StringField, BooleanField, PasswordField, EmailField, validators, SubmitField, TextAreaField, SelectField


class RegisterForm(FlaskForm):
    """Register User"""

    name = StringField("Name",
                       validators=[validators.DataRequired()])

    username = StringField("Username",
                           validators=[validators.DataRequired()])

    email = EmailField("Email",
                       validators=[validators.DataRequired(), Email()])

    address = StringField("Address",
                          validators=[validators.DataRequired()])

    password = PasswordField("Password",
                             validators=[validators.DataRequired()])


class LoginForm(FlaskForm):
    """Login User"""

    username = StringField("Username",  validators=[validators.DataRequired()])

    password = PasswordField("Password",  validators=[
                             validators.DataRequired()])

    remember_me = BooleanField('Remeber Me')


class UpdateAccountForm(FlaskForm):
    """Update User"""

    email = EmailField("Email",
                       validators=[validators.DataRequired(), Email()])

    address = StringField("Address",
                          validators=[validators.DataRequired()])

    password = PasswordField("Password",
                             validators=[validators.DataRequired()])


class ContactForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    phone = StringField("Phone")
    reason = SelectField('Reason for Contact', choices=[('default', 'Select the reason for contact'), (
        'suggestion', 'Suggestion'), ('complaint', 'Complaint'), ('question', 'Question')])
    description = TextAreaField("Describe the reason for contact..")
    submit = SubmitField('Submit')

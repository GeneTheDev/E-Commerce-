from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
from .forms import RegisterForm, LoginForm, UpdateAccountForm

from email_validator import validate_email, EmailNotValidError
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import psycopg2
import psycopg2.extras

from . import create_app
app = create_app()


def validate_email_address(email):
    try:
        # Validate the email address
        valid = validate_email(email)

        # Get the normalized email address
        email = valid.email

        # Return the normalized email address
        return email

    except EmailNotValidError as e:
        # Email is not valid, raise an exception
        raise Exception(str(e))


if __name__ == '__main__':
    app.run()

from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension

from email_validator import validate_email, EmailNotValidError
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import psycopg2
import psycopg2.extras

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__, template_folder='templates',
                static_url_path='/static')
    app.config['SECRET_KEY'] = '<replace with a secret key>'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gene:password@127.0.0.1/32/webstore_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.debug = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints
    from products import products_bp
    from auth import auth_bp
    from cart import cart_bp
    from home import home_bp
    from contact import contact_bp
    app.register_blueprint(products_bp, url_prefix="/")
    app.register_blueprint(cart_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(contact_bp, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app


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


app = create_app()

if __name__ == '__main__':
    app.run()

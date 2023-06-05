import psycopg2.extras
import psycopg2
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
from flask_session import Session
from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from auth import auth_bp, load_user, load_user_from_request
import os
from extensions import db, bcrypt, login_manager
import sys
sys.path.insert(0, "/home/gene/web_store/")


def create_app():

    app = Flask(__name__, template_folder='templates',
                static_url_path='/static')
    app.config['SECRET_KEY'] = 'secret'
    app.config['WTF_CSRF_SECRET_KEY'] = 'your-secret-key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql:///webstore_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.debug = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.user_loader(load_user)
    login_manager.request_loader(load_user_from_request)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints
    from products import products_bp
    from auth import auth_bp
    from cart import cart_bp
    from home import home_bp
    from contact import contact_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(contact_bp)

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

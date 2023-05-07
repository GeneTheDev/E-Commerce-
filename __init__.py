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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///webstore_db'
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
    from .products import products_bp
    from .auth import auth_bp
    from .cart import cart_bp
    from .home import home_bp
    from .contact import contact_bp
    app.register_blueprint(products_bp, )
    app.register_blueprint(cart_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(contact_bp, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app

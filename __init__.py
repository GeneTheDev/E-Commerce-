from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()

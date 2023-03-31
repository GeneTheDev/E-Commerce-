from flask import Blueprint, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import Flask, Blueprint, render_template, abort, request
from ..models import Product


home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@home_bp.route("/")
def home():
    """Home page"""
    featured_products = Product.query.filter_by(is_featured=True).all()
    for product in featured_products:
        product.image_url = url_for(
            'static', filename='images/' + product.image)

    return render_template('index.html', featured_products=featured_products, current_user=current_user)

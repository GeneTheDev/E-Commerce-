from flask import Flask, Blueprint, render_template, abort, request
from ..models import Product


products_bp = Blueprint('products', __name__,
                        template_folder='templates',
                        static_folder='static')


@products_bp.route("/products")
def product_page():
    """Product page"""
    return render_template("products.html")


@products_bp.route("/allproducts")
def all_products():
    products = Product.query.all()
    category_filter = request.args.get('category')
    price_filter = request.args.get('price')
    rating_filter = request.args.get('rating')
    return render_template('allproducts.html', products=products, category_filter=category_filter, price_filter=price_filter, rating_filter=rating_filter)


@products_bp.route('/next')
def next_page():
    return render_template('next.html')


@products_bp.route("/product-detail/<int:product_id>")
def product_detail(product_id):
    """Product page"""
    product = Product.query.get(product_id)
    if not product:
        abort(404)
    return render_template("/singleproduct.html", product=product)

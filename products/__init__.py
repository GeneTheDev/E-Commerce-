from flask import Flask, Blueprint, render_template, abort, request
from ..models import Product
from flask_paginate import Pagination, get_page_parameter


products_bp = Blueprint('products', __name__,
                        template_folder='templates',
                        static_folder='static')


@products_bp.route("/products")
def product_page():
    """Product page"""
    return render_template("products.html")


PER_PAGE = 8


@products_bp.route("/allproducts")
def all_products():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * PER_PAGE
    total_products = Product.query.count()
    pagination = Pagination(page=page, total=total_products,
                            search=search, record_name='products')

    products = Product.query.order_by(
        Product.id).offset(offset).limit(PER_PAGE).all()
    category_filter = request.args.get('category')
    price_filter = request.args.get('price')
    rating_filter = request.args.get('rating')
    return render_template('allproducts.html', products=products, category_filter=category_filter, price_filter=price_filter, rating_filter=rating_filter, pagination=pagination, offset=offset)


@products_bp.route("/product-detail/<int:product_id>")
def product_detail(product_id):
    """Product page"""
    product = Product.query.get(product_id)
    if not product:
        abort(404)
    return render_template("/singleproduct.html", product=product)

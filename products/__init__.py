from flask import Flask, Blueprint, render_template, abort, request
from models import Product
from flask_paginate import Pagination, get_page_parameter


products_bp = Blueprint('products', __name__,
                        template_folder='templates',
                        static_folder='static')


@products_bp.route("/product")
def product_page():
    """Product page"""
    return render_template("product.html")


@products_bp.route("/allproducts")
def all_products():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    PER_PAGE = 8
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * PER_PAGE

    products_query = Product.query

    category_filter = request.args.get('category')
    if category_filter:
        products_query = products_query.filter(
            Product.category == category_filter)

    price_filter = request.args.get('price')
    if price_filter:
        if price_filter == "asc":
            products_query = products_query.order_by(Product.price.asc())
        elif price_filter == "desc":
            products_query = products_query.order_by(Product.price.desc())

    rating_filter = request.args.get('rating')
    if rating_filter:
        if rating_filter == "asc":
            products_query = products_query.order_by(Product.rating.asc())
        elif rating_filter == "desc":
            products_query = products_query.order_by(Product.rating.desc())

    total_products = products_query.count()
    pagination = Pagination(page=page, total=total_products,
                            search=search, record_name='products')

    products = products_query.offset(offset).limit(PER_PAGE).all()

    return render_template('allproducts.html', products=products, category_filter=category_filter, price_filter=price_filter, rating_filter=rating_filter, pagination=pagination, offset=offset)


@products_bp.route("/product-detail/<int:product_id>")
def product_detail(product_id):
    """Product page"""
    product = Product.query.get(product_id)
    related_products = product.related_products()
    if not product:
        abort(404)
    return render_template("/singleproduct.html", product=product, related_products=related_products)

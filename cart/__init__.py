from flask import Flask, Blueprint, render_template, abort, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from ..models import db, CartItem, Cart, Product

cart_bp = Blueprint('cart_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@cart_bp.route('/cart')
def view_cart():

    if current_user.is_authenticated:
        cart = Cart.query.filter_by(customer_id=current_user.id).first()
        if cart:
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            total_cost = sum(item.product.price *
                             item.qauntity for item in cart_items)
        else:
            cart_items = []
            total_cost = 0
    else:
        cart_items = []
        total_cost = 0

    return render_template('cart.html', cart_items=cart_items, total_cost=total_cost)


# Add Items to shopping cart


@cart_bp.route('/add_to_cart/<string:code>', methods=['POST'])
def add_to_cart(code):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    product = Product.query.filter_by(code=code).first()
    if product:
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, product_id=product.id).first()
        if not cart_item:
            cart_item = CartItem(user_id=current_user.id,
                                 product_id=product.id)
            db.session.add(cart_item)
        else:
            cart_item.quantity += 1
        db.session.commit()
        return redirect(url_for('shopping_cart'))
    else:
        abort(404)

# Empty the entire cart


@cart_bp.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)

# Delete products from cart


@cart_bp.route('/delete/<string:code>', methods=['POST'])
def delete_from_cart(code):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    product = Product.query.filter_by(code=code).first()
    if product:
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, product_id=product.id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
        return redirect(url_for('shopping_cart'))
    else:
        abort(404)

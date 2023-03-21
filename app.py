from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from flask_session import Session
from models import db, connect_db, Product, Order, Customer, Category, ProductCategory, OrderProduct, Address, Payment, User, Cart, CartItem
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, UpdateAccountForm
from email_validator import validate_email, EmailNotValidError
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import psycopg2  # pip install psycopg2
import psycopg2.extras


app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///webstore_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.debug = True


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

Session(app)
toolbar = DebugToolbarExtension(app)


connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    # Check if there is a user_id in the request headers
    user_id = request.headers.get('Authorization')
    if user_id:
        return User.query.get(int(user_id))
    else:
        return None


@app.route("/")
def home():
    """Home page"""
    featured_products = Product.query.filter_by(is_featured=True).all()
    for product in featured_products:
        product.image_url = url_for(
            'web_store/static/images', filename=product.image)

    return render_template('index.html', featured_products=featured_products, current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form and handle form submission"""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        address = form.address.data

        user = Customer(name=name, username=username, email=email,
                        password_hash=password, address=address)

        db.session.add(user)
        db.session.commit()

        # on successful registration, redirect to login page
        return redirect("/login")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login"""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = Customer.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
            # on successful login, redirect to home page

        else:
            # re-render the login page with an error
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", title='Sign In', form=form)


@app.route('/logout')
def logout():
    """Logs out user and redirects to homepage"""
    session.pop("user_id")
    return redirect("/")


@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address

    return render_template('update_account.html', form=form)


@app.route("/account", methods=['GET'])
def account_page():
    """Account page"""
    form = UpdateAccountForm()
    return render_template("/account.html", form=form)

# Shopping cart


@app.route('/cart')
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


@app.route('/add_to_cart/<string:code>', methods=['POST'])
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


@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)

# Delete products from cart


@app.route('/delete/<string:code>', methods=['POST'])
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


@app.route("/products")
def product_page():
    """Product page"""
    return render_template("products.html")


@app.route("/allproducts")
def all_products():
    products = Product.query.all()
    category_filter = request.args.get('category')
    price_filter = request.args.get('price')
    rating_filter = request.args.get('rating')
    return render_template('allproducts.html', products=products, category_filter=category_filter, price_filter=price_filter, rating_filter=rating_filter)


@app.route('/next')
def next_page():
    return render_template('next.html')


@app.route("/product-detail")
def product_detail():
    """Product page"""
    return render_template("/singleproduct")


@app.route("/contact")
def contact_page():
    """Contact page"""
    return render_template("/contact.html")


if __name__ == '__main__':
    app.run()

from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_session import Session
from models import db, connect_db, Product, Order, Customer, Category, ProductCategory, OrderProduct, Address, Payment, User, Cart, CartItem
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, UpdateAccountForm
from email_validator import validate_email, EmailNotValidError
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


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
def shopping_cart():
    """Display cart"""

    cart = Cart.query.filter_by(customer_id=current_user.id).first()
    if not cart:
        flash('Youe cart is empty', 'info')
    return render_template('cart.html')


@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add Item to cart"""

    product = Product.query.get_or_404(product_id)

    cart = Cart.query.filter_by(customer_id=current_user.id).first()

    if not cart:
        cart = Cart(customer_id=current_user.id)
        db.session.add(cart)

    cart_item = CartItem.query.filter_by(
        product_id=product.id, cart_id=cart.id).first()

    if cart_item:
        cart_item.qauntity += 1

    else:
        cart_item = CartItem(product_id=product.id, cart_id=cart.id)

    db.session.add(cart_item)
    db.session.commit()

    flash(f'{product.name} added to cart!', 'success')

    return redirect(url_for('product_detail', id=product_id))


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


# @app.route("/product/<int:id>")
# def product():
#     product = Product.query.filter_by(id=id).first()
#     render_template('product.html', product=product)


@app.route('/next')
def next_page():
    return render_template('next.html')


@app.route("/product-detail")
def product_detail():
    """Product page"""
    return render_template("/singleproduct.html")


@app.route("/about")
def about_page():
    """About page"""
    return render_template("/about.html")


@app.route("/contact")
def contact_page():
    """Contact page"""
    return render_template("/contact.html")


if __name__ == '__main__':
    app.run()

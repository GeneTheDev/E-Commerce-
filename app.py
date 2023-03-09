from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_session import Session
from models import db, connect_db, Product, Order, Customer, Category, ProductCategory, OrderProduct, Address, Payment, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm
from email_validator import validate_email, EmailNotValidError
from flask_login import LoginManager, login_user, logout_user, current_user


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

    if current_user.is_authenticated:
        return redirect(url_for('index'))

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

    return render_template("login.html", title='Sign In', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
    print(f"Category Filter: {category_filter}")
    print(f"Price Filter: {price_filter}")
    print(f"Rating Filter: {rating_filter}")
    print(f"Request: {request}")
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


@app.route("/account")
def account_page():
    """Account page"""
    return render_template("/account.html")


if __name__ == '__main__':
    app.run()

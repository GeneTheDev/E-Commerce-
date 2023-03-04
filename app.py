from flask import Flask, request, redirect, render_template, url_for, session
from models import db, connect_db, Product, Order, Customer, Category, ProductCategory, OrderProduct, Address, Payment
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm


app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///webstore_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
toolbar = DebugToolbarExtension(app)


connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()


@app.route("/")
def home():
    """Home page"""
    featured_products = Product.query.filter_by(is_featured=True).all()
    for product in featured_products:
        product.image_url = url_for(
            'web_store/static/images', filename=product.image)
    return render_template('index.html', featured_products=featured_products)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form and handle form submission"""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data

        user = Customer(username=name, email=email, password=pwd)
        db.session.add(user)
        db.session.commit()

        # on successful login, redirect to home page
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
            session["customer_id"] = user.id
            return redirect("/index.html")
            # on successful login, redirect to home page

        else:
            # re-render the login page with an error
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

# @app.route("/")
# def home():
#     """Home page"""
#     featured_products = Product.query.all()
#     # Adding some dummy data to the Product table
#     product1 = Product(name='Product 1', description='Description for Product 1',
#                        price=10.0, image='product1.jpg', availability=True, rating=4.0, is_featured=True)
#     product2 = Product(name='Product 2', description='Description for Product 2',
#                        price=20.0, image='product2.jpg', availability=True, rating=3.5, is_featured=True)

#     db.session.add_all([product1, product2])
#     db.session.commit()

#     return render_template('index.html', featured_products=featured_products)


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

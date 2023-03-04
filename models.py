from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy()


class User(db.Model):
    """Site user"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.Text,
                         nullable=False,
                         unique=True)

    password = db.Column(db.Text,
                         nullable=False)


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(50),
                     nullable=False)

    description = db.Column(db.String,
                            nullable=False)

    price = db.Column(db.Float,
                      nullable=False)

    image = db.Column(db.String,
                      nullable=False)

    availability = db.Column(db.Boolean,
                             nullable=False,
                             default=True)

    rating = db.Column(db.Float,
                       default=0.0)

    is_featured = db.Column(db.Boolean,
                            default=True)

    categories = db.relationship("ProductCategory",
                                 back_populates='product')

    orders = db.relationship('OrderProduct',
                             back_populates='product')


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String)

    email = db.Column(db.String,
                      unique=True,
                      nullable=False)

    name = db.Column(db.String, nullable=False)

    password = db.Column(db.String, nullable=False)

    address = db.Column(db.String, nullable=False)

    orders = db.relationship("Order")

    addresses = db.relationship("Address")

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    def authenticate(cls, username, pwd):
        """Validate that user exists and password is correct

        Return user if valid; else return False
        """

        u = Customer.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)

    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customers.id'),
                            nullable=False)

    total_cost = db.Column(db.Float,
                           nullable=False)

    order_date = db.Column(db.String,
                           nullable=False)

    customer = db.relationship("Customer",
                               overlaps='orders')

    order_products_backref = db.relationship("OrderProduct",
                                             backref="order")

    payment = db.relationship("Payment")


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String, nullable=False)

    products = db.relationship("ProductCategory")


class ProductCategory(db.Model):

    __tablename__ = 'product_categories'

    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id'),
                           primary_key=True)

    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id'),
                            primary_key=True)

    product = db.relationship("Product",
                              back_populates="categories")

    category = db.relationship("Category", overlaps="products")

    __table_args__ = (
        db.UniqueConstraint('product_id', 'category_id'),
    )


class OrderProduct(db.Model):

    __tablename__ = 'order_products'

    order_id = db.Column(db.Integer,
                         db.ForeignKey('orders.id'),
                         primary_key=True)

    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id'),
                           primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)

    price = db.Column(db.Float, nullable=False)

    product = db.relationship("Product",
                              back_populates="orders")

    __table_args__ = (
        db.UniqueConstraint('order_id', 'product_id'),
    )


class Address(db.Model):

    __tablename__ = 'addresses'

    customer_email = db.Column(db.String,
                               db.ForeignKey('customers.email'),
                               primary_key=True)

    type = db.Column(db.String,
                     primary_key=True)

    address = db.Column(db.String,
                        nullable=False)

    customer = db.relationship("Customer",
                               overlaps='addresses')


class Payment(db.Model):

    __tablename__ = 'payments'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    order_id = db.Column(db.Integer,
                         db.ForeignKey('orders.id', ondelete='CASCADE'),
                         nullable=False)

    amount = db.Column(db.Float,
                       nullable=False)

    payment_date = db.Column(db.String,
                             nullable=False)

    order = db.relationship("Order",
                            overlaps='payment')


def connect_db(app):
    """Connect to database."""
    db.init_app(app)
    db.app = app

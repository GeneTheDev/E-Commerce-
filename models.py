
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from . import db

bcrypt = Bcrypt()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    """Site user"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String(64),
                         index=True,
                         unique=True)

    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return 'User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String)

    email = db.Column(db.String,
                      unique=True,
                      nullable=False)

    name = db.Column(db.String,
                     nullable=False)

    password_hash = db.Column(db.String(128),
                              nullable=False)

    is_active = db.Column(db.Boolean,
                          default=True,
                          nullable=False)

    address = db.Column(db.String,
                        nullable=False)

    orders = db.relationship("Order")

    addresses = db.relationship("Address")

    def __init__(self, username, email, name, password, address):
        self.username = username
        self.email = email
        self.name = name
        self.set_password(password)
        self.address = address

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def get_id(self):
        return str(self.id)

    @classmethod
    def register(cls, username, pwd, email, name, address):
        """Register user w/hashed password & return user"""
        user = cls(username=username, email=email, name=name, address=address)

        hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        hashed_utf8 = hashed.decode('utf-8')

        user.password = hashed_utf8

        db.session.add(user)
        db.session.commit()

        cart = Cart(customer_id=user.id)
        db.session.add(cart)
        db.session.commit()

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct

        Return user if valid; else return False
        """

        user = Customer.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            # return user instance
            return user
        else:
            return False


class Cart(db.Model):
    """Shopping cart"""

    __tablename__ = 'carts'

    id = db.Column(db.Integer,
                   primary_key=True)

    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customers.id'),
                            nullable=False)

    items = db.relationship('CartItem',
                            backref='cart', lazy=True)


class CartItem(db.Model):
    """Cart Item model"""

    __tablename__ = 'cart_items'

    id = db.Column(db.Integer,
                   primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),
                           nullable=False)

    cart_id = db.Column(db.Integer,
                        db.ForeignKey('carts.id'),
                        nullable=False)

    qauntity = db.Column(db.Integer,
                         nullable=False,
                         default=1)

    product = db.relationship('Product', backref='cart_items')


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

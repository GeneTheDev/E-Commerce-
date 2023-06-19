from flask import Blueprint, render_template, url_for, session, redirect, request, flash
from flask_login import login_user, current_user, login_required
from forms import RegisterForm, LoginForm, UpdateAccountForm
from models import db, Customer, User
from flask import Flask, Blueprint, render_template, abort, request
from flask import current_app as app


auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


def load_user(user_id):
    return User.query.get(int(user_id))


def load_user_from_request(request):
    # Check if there is a user_id in the request headers
    user_id = request.headers.get('Authorization')
    if user_id:
        return User.query.get(int(user_id))
    else:
        return None


@auth_bp.route("/register", methods=["GET", "POST"])
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
                        password=password, address=address)

        db.session.add(user)
        db.session.commit()

        # on successful registration, redirect to login page
        return redirect("/login")

    else:
        return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
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


@auth_bp.route('/logout')
def logout():
    """Logs out user and redirects to homepage"""
    session.pop("user_id")
    return redirect("/")


@auth_bp.route('/update_account', methods=['POST'])
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


@auth_bp.route("/account", methods=['GET'])
def account_page():
    """Account page"""
    form = UpdateAccountForm()
    return render_template("/account.html", form=form)

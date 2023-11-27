from flask import Flask, render_template, redirect, url_for, request, session, abort, jsonify
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView
import os
from api import api
from models import strg
from models.user import User, Role
from models.cart import Cart
from models.product import Product
from models import strg
from models.category import Category
from models.cart_item import CartItem
from app.forms.user_forms import LoginForm, RegisterForm
from models.custom_view import CustomView
import random

app = Flask(__name__)

# Load configuration from a separate file (e.g., config.py)
app.config.from_pyfile('config.py')

login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return strg.session.query(User).get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = strg.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                # if user.password == form.password.data:
                login_user(user, remember=form.rememberMe.data)
                next_url = session.pop(
                    'next', None) or url_for("index")
                return redirect(next_url)
        return "password or uesrname is incorrect"
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        if user:
            return "Your account has been created successfully <br>You can login now!"
        return "Something went wrong! Please try again later or contact support."
    return render_template("register.html", form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("index"))


class myAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


def create_admin(app):
    from flask_admin.contrib.sqla import ModelView

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(CustomView(User))
    admin.add_view(CustomView(Cart))
    admin.add_view(CustomView(Product))


create_admin(app)

# Register API blueprint
app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False


@app.route("/")
@app.route("/home")
def index():
    categories = strg.search(cls=Category, parent_id=None)
    popular = random.sample(strg.all(Product), 8)
    return render_template("home.html", current_user=current_user, categories=categories, popular=popular)


@app.route("/product/<id>")
def product_page(id):
    product=strg.search(cls=Product, id=id)
    popular = random.sample(strg.all(Product), 5)
    return render_template("product_details.html", product=product, popular=popular)


@app.route("/myCart")
@login_required
def my_cart():
    """Cart method"""
    cart = current_user.cart
    items = current_user.cart.cart_items
    return render_template("my_cart.html", current_user=current_user, items=items, cart=cart)


@app.route('/add_to_cart/<uuid:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = db.session().query(Product).get(product_id)
    product.add_to_cart(current_user)
    strg.save()
    return jsonify({'success': True, 'cart_count': current_user.cart.total_items})


@app.route('/remove_from_cart/<uuid:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    product = db.session().query(Product).get(product_id)
    product.remove_from_cart(current_user)
    strg.save()
    return jsonify({'success': True, 'cart_count': current_user.cart.total_items})


@app.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized access to redirect to login page"""
    session['next'] = request.url
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

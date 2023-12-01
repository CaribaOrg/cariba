from flask import Flask, render_template, redirect, url_for, request, session, g, jsonify
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView
import os
from api import api
from models import strg
from models.user import User
from models.cart import Cart
from models.car import Car
from models.product import Product
from models import strg
from models.category import Category
from models.cart_item import CartItem
from app.forms.user_forms import LoginForm, RegisterForm
from models.custom_view import CustomView
import random

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Load configuration from a separate file (e.g., config.py)
app.config.from_pyfile('app/config.py')
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return strg.session.query(User).get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = strg.session.query(User).filter_by(
            username=form.username.data).first()
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
            return redirect(url_for('redirect_page'))
        return "Something went wrong! Please try again later or contact support."
    return render_template("register.html", form=form)


@app.route("/redirect", methods=['GET'])
def redirect_page():
    return render_template("redirect.html")


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
    admin.add_view(CustomView(Car))



create_admin(app)

# Register API blueprint
app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False

@app.route("/")
@app.route("/home")
def index():
    categories = strg.search(cls=Category, parent_id=None)
    popular = random.sample(supported_products(strg.all(Product)), 8)
    return render_template("home.html", current_user=current_user, categories=categories, popular=popular)


@app.route("/product/<uuid:id>")
def product_page(id):
    # product = strg.search(cls=Product, id=id) // search needs a fix
    product = strg.session().query(Product).get(id)
    popular = random.sample(supported_products(strg.all(Product)), 5)
    return render_template("product_details.html", product=product, popular=popular, current_user=current_user)


@app.route("/myCart")
@login_required
def my_cart():
    """Cart method"""
    cart = current_user.cart
    items = current_user.cart.cart_items
    return render_template("my_cart.html", current_user=current_user, items=items, cart=cart)


@app.route('/add_to_cart/<uuid:product_id>/<int:quantity>', methods=['POST'])
@login_required
def add_to_cart(product_id, quantity=1):
    """add an element to the cart"""
    product = strg.session().query(Product).get(product_id)
    product.add_to_cart(current_user, quantity)
    strg.save()
    return jsonify({'success': True, 'cart_count': current_user.cart.total_items})


@app.route('/remove_from_cart/<uuid:product_id>/<int:quantity>', methods=['POST'])
@login_required
def remove_from_cart(product_id, quantity=1):
    """remove an element from the cart"""
    product = strg.session().query(Product).get(product_id)
    product.remove_from_cart(current_user, quantity)
    strg.save()
    return jsonify({'success': True, 'cart_count': current_user.cart.total_items})


@app.route('/categories', defaults={'category': None})
@app.route('/categories/<category>')
def categories(category):
    categories = strg.search(cls=Category, parent_id=None)
    if category is None:
        current_category = strg.session.query(Category).first()
    else:
        current_category = strg.session.query(
            Category).filter_by(name=category).first()
    prod_list = get_products(current_category, [])
    return render_template('categories.html', prod_list=prod_list, current_user=current_user, current_category=current_category, categories=categories)


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized access to redirect to login page"""
    session['next'] = request.url
    return redirect(url_for('login'))


def get_products(cat, prods):
    prods.extend(supported_products(cat.products))
    for sub_cat in cat.children:
        prods = get_products(sub_cat, prods)
    return prods

def supported_products(prod_list):
    if not current_user.is_authenticated or not current_user.cars:
        return prod_list
    support_list = []
    for car in current_user.cars:
        for prod in prod_list:
            if car.make.lower() in prod.support and prod not in support_list:
                support_list.append(prod)
    return support_list
                
        


@app.route("/addCar", methods=['POST'])
@login_required
def add_car():
    form_data = request.form.to_dict()
    form_data['user_id'] = current_user.id
    Car(**form_data)
    strg.save()
    return redirect(url_for('garage'))

@app.route("/myGarage")
@login_required
def garage():
    cars = current_user.cars
    return render_template('garage.html', cars=cars)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

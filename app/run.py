from requests.auth import HTTPBasicAuth
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from flask_admin import Admin
# from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView
import requests
from api import api
from models import strg
from models.user import User, Role
from models.cart import Cart
from models.car import Car
from models.product import Product
from models import strg
from models.category import Category
from models.order import Order
from app.forms.user_forms import SubscriptionForm
from models.custom_view import CustomView
import random
from flask_security import Security, current_user, auth_required, SQLAlchemySessionUserDatastore, login_required
from flask_mailman import Mail, EmailMessage


app = Flask(__name__)

app.config.from_pyfile('config.py')

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: strg.session.close())


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(strg.session, User, Role)
app.security = Security(app, user_datastore)
mail = Mail(app)

# login = LoginManager(app)


@app.security.login_manager.user_loader
def load_user(user_id):
    return strg.session.query(User).get(user_id)


@app.route("/redirect", methods=['GET'])
def redirect_page():
    return render_template("redirect.html")


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
    admin.add_view(CustomView(Order))


create_admin(app)

# Register API blueprint
app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False


@app.route("/")
@app.route("/home")
def index():
    categories = strg.search(cls=Category, parent_id=None)
    popular_products = supported_products(strg.all(Product))
    if not popular_products or len(popular_products) < 10:
        sample_size = len(popular_products)
    else:
        sample_size = 10
    popular = random.sample(popular_products, sample_size)
    return render_template("home.html", current_user=current_user, categories=categories, popular=popular)


@app.route("/product/<uuid:id>")
def product_page(id):
    # product = strg.search(cls=Product, id=id) // search needs a fix
    product = strg.session().query(Product).get(id)
    popular_products = supported_products(strg.all(Product))
    if not popular_products or len(popular_products) < 5:
        sample_size = len(popular_products)
    else:
        sample_size = 5
    popular = random.sample(popular_products, sample_size)
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
    if not isinstance(prod_list, list):
        prod_list = [prod_list]
    if not current_user.is_authenticated or len(current_user.cars) == 0:
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


@app.route("/editCar/<uuid:car_id>", methods=['POST'])
@login_required
def edit_car(car_id):
    form_data = request.form.to_dict()
    car = strg.session().query(Car).get(car_id)
    for key, value in form_data.items():
        if getattr(car, key) != value:
            setattr(car, key, value)
    strg.save()
    return redirect(url_for('garage'))


@app.route("/deleteCar/<uuid:car_id>")
@login_required
def delete_car(car_id):
    car = strg.session().query(Car).get(car_id)
    car.delete()
    return redirect(url_for('garage'))


@app.route("/myGarage")
@login_required
def garage():
    cars = current_user.cars
    return render_template('garage.html', cars=cars)


@app.route("/checkout")
@login_required
def checkout():
    cart = current_user.cart
    items = current_user.cart.cart_items
    return render_template("checkout.html", current_user=current_user, items=items, cart=cart)


@app.route("/payments/<order_id>/capture", methods=["POST"])
@login_required
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = paypal_capture_function(order_id)
    # print(captured_payment)
    if is_approved_payment(captured_payment):
        # Do something (for example Update user field)
        current_user.cart.checkout(captured_payment.get("status"))
    return jsonify(captured_payment)


def paypal_capture_function(order_id):
    post_route = f"/v2/checkout/orders/{order_id}/capture"
    paypal_capture_url = app.config["PAYPAL_API_URL"] + post_route
    basic_auth = HTTPBasicAuth(
        app.config["PAYPAL_BUSINESS_CLIENT_ID"], app.config["PAYPAL_BUSINESS_SECRET"])
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url=paypal_capture_url,
                             headers=headers, auth=basic_auth)
    response.raise_for_status()
    json_data = response.json()
    return json_data


def is_approved_payment(captured_payment):
    status = captured_payment.get("status")
    amount = captured_payment.get("purchase_units")[0].get(
        "payments").get("captures")[0].get("amount").get("value")
    currency_code = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get(
        "currency_code")
    print(f"Payment happened. Details: {status}, {amount}, {currency_code}")
    if status == "COMPLETED":
        return True
    else:
        return False


@app.route("/search", methods=['POST'])
def search():
    search_dict = {
        'cls': Product,
        'case_sensitive': False,
        'exact': False
    }
    search_dict['name'] = request.form.get('name')
    products = strg.search(**search_dict)
    if current_user.is_authenticated:
        products = supported_products(products)
    categories = strg.search(cls=Category, parent_id=None)
    return render_template('search.html', products=products, search_input=request.form.get('name'), categories=categories)


@app.route("/myOrders")
@login_required
def orders():
    orders = current_user.orders
    return render_template('orders.html', orders=orders)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to the newsletter endpoint"""
    email = request.form.get('email')
    # Send a confirmation email
    emailSent = send_confirmation_email(email)
    if emailSent:
        flash('Subscription successful! Check your email for confirmation.', "Success")
    else:
        flash('Something went wrong, please try again later.', "Error")
    return redirect(url_for('index'))


def send_confirmation_email(email):
    """send a confirmation email for successful subscription"""
    try:
        subject, from_email, to = 'Subscription Confirmation', 'noreply@fuzzfoo.tech', email
        html_content = '<h1>Thank you for subscribing to our newsletter!</h1> <p>Cariba Team</p>'
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html"
        msg.send()
        return True
    except Exception:
        return False


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

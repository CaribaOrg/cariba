from requests.auth import HTTPBasicAuth
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import requests
from api import api
from models.user import User, Role
from models.cart import Cart
from models.car import Car
from models.product import Product
from models import strg
from models.category import Category
from models.order import Order
from models.wishlist import WishlistItem
from models.address import Address
import random
from flask_security import Security, current_user, SQLAlchemySessionUserDatastore, login_required
from flask_mailman import Mail, EmailMessage
from functools import wraps
from models.notification import Message, Notification
from datetime import datetime
from flask_ckeditor import CKEditor


app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

app.config.from_pyfile('app/config.py')

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: strg.session.close())


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(strg.session, User, Role)
app.security = Security(app, user_datastore)

mail = Mail(app)
ckeditor = CKEditor(app)


# login = LoginManager(app)


@app.security.login_manager.user_loader
def load_user(user_id):
    return strg.session.query(User).get(user_id)


class myAdminView(ModelView):
    def is_accessible(self):
        """Check if current user is an admin"""
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login"))


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        """Check if the current user is an admin"""
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page if the user is not an admin"""
        return redirect(url_for("security.login"))


def create_admin(app):
    admin = Admin(app, name='Admin', template_mode='bootstrap3',
                  index_view=CustomAdminIndexView())
    admin.add_view(myAdminView(User, strg.session))
    admin.add_view(myAdminView(Cart, strg.session))
    admin.add_view(myAdminView(Product, strg.session))
    admin.add_view(myAdminView(Car, strg.session))
    admin.add_view(myAdminView(Order, strg.session))
    admin.add_view(myAdminView(Address, strg.session))
    admin.add_view(myAdminView(WishlistItem, strg.session))


create_admin(app)

# Register API blueprint
app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please login to access this page.", "Info")
            return redirect(url_for('security.login'))
        return f(*args, **kwargs)
    return decorated_function


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
    product = strg.session().query(Product).get(id)
    popular_products = supported_products(strg.all(Product))
    if not popular_products or len(popular_products) < 5:
        sample_size = len(popular_products)
    else:
        sample_size = 5
    popular = random.sample(popular_products, sample_size)
    supported_cars = []
    if current_user.is_authenticated:
        for car in current_user.cars:
            if product.is_supported(car):
                supported_cars.append(car)
    return render_template("product_details.html", product=product, popular=popular, current_user=current_user, supported_cars=supported_cars)


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
    if len(items) == 0:
        return redirect(url_for('my_cart'))
    return render_template("checkout.html", current_user=current_user, items=items, cart=cart)


@app.route("/payments/<order_id>/capture", methods=["POST"])
@login_required
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = paypal_capture_function(order_id)
    # print(captured_payment)
    if is_approved_payment(captured_payment):
        # Do something (for example Update user field)
        current_user.cart.checkout(captured_payment.get("status"))
        author = current_user
        recipient = current_user
        body = "<h1>Order successful!!</h1>"
        title = "Payment Succesful"
        label = "payments"
        Message(author=author, recipient=recipient, body=body, title=title, message_label=label)
        strg.save()
        recipient.add_notification('unread_message_count',
                            recipient.unread_message_count())
        strg.save()
    else:
        author = current_user
        recipient = current_user
        body = "<h1>Order unsuccessful!!</h1>"
        title = "Payment Unsuccesful"
        label = "payments"
        Message(author=author, recipient=recipient, body=body, title=title, message_label=label)
        strg.save()
        recipient.add_notification('unread_message_count',
                            recipient.unread_message_count())
        strg.save()
        
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
    return render_template('search.html',
                           products=products,
                           search_input=request.form.get('name'),
                           categories=categories)


@app.route("/myOrders")
@login_required
def orders():
    orders = current_user.orders
    return render_template('orders.html', orders=orders)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        for key, value in form_data.items():
            if hasattr(current_user.address, key):
                setattr(current_user.address, key, value)
            else:
                setattr(current_user, key, value)
        strg.save()
        flash('Information saved successfully', 'Success')
        return redirect(url_for('account'))
    return render_template('account.html', user=current_user)


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


@app.route("/about")
def about():
    """About us page."""
    return render_template("about.html")


@app.route("/buyAgain/<uuid:order_id>")
@login_required
def buy_again(order_id):
    """order again"""
    order = strg.session().query(Order).get(order_id)
    for item in order.cart.cart_items:
        item.product.add_to_cart(current_user, item.quantity)
    return redirect(url_for('my_cart'))


@app.route("/favourites")
@login_required
def wishlist():
    return render_template("favourites.html", current_user=current_user)


@app.route("/add_to_favourites/<uuid:id>", methods=['POST'])
@login_required
def add_to_wishlist(id):
    product = strg.session().query(Product).get(id)
    product.add_to_wishlist(current_user)
    return '', 200


@app.route("/remove_from_favourites/<uuid:id>", methods=['POST'])
@login_required
def remove_from_wishlist(id):
    product = strg.session().query(Product).get(id)
    product.remove_from_wishlist(current_user)
    return '', 200


@app.errorhandler(404)
def notfound(error):
    """Handle the error 404"""
    return render_template("404.html"), 404


@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    strg.save()
    # .order_by(Message.updated_at.desc())
    messages = current_user.messages_received
    return render_template('messages.html', messages=messages, current_user=current_user)


@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    query = strg.session.query(Notification).filter(
        Notification.updated_at > since).order_by(Notification.updated_at.asc())
    notifications = strg.session.scalars(query)
    return [{
        'name': n.name,
        'data': n.get_data(),
        'updated_at': n.updated_at
    } for n in notifications]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

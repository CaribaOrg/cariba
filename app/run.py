from flask import Flask, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemySessionUserDatastore
import os
from api import api
from models import strg
from models.user import User, Role

app = Flask(__name__)

# Load configuration from a separate file (e.g., config.py)
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)


def create_admin(app, db):
    from flask_admin.contrib.sqla import ModelView

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    # Add other views as needed


create_admin(app, db)

# Register API blueprint
app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False


@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")


@app.route("/product/<name>")
def product_page(name):
    return render_template("product_details.html", product_name=name)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

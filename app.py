#!/usr/bin/python3

from flask import Flask, request, render_template
from models import strg
from flask_login import LoginManager
from api import api
from flask_login import login_user, logout_user
from models.user import User, Role
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
# Don't worry if email has findable domain
app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(strg, User, Role)
app.security = Security(app, user_datastore)

# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{current_user.email}}!')

@app.route("/user")
@auth_required()
@permissions_accepted("user-read")
def user_home():
    return render_template_string("Hello {{ current_user.email }} you are a user!")

# one time setup
with app.app_context():
    init_db()
    # Create a user and role to test with
    app.security.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )
    strg.commit()
    if not app.security.datastore.find_user(email="test@me.com"):
        app.security.datastore.create_user(email="test@me.com",
        password=hash_password("password"), roles=["user"])
    strg.commit()

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    strg.close()

@app.errorhandler(404)
def error(err):
    return 'oops, nothing here', 404

with app.app_context():
    app.security.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )

    app.security.datastore.find_or_create_role(
        name="admin", permissions={"user-read", "user-write", "admin-read", "admin-write"}
    )
    strg.save()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

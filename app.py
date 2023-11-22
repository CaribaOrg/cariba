#!/usr/bin/python3

from flask import Flask, request, render_template
from models import strg
from flask_login import LoginManager
from api import api
from flask_login import login_user, logout_user
from models.user import User

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False

# app.config["SECRET_KEY"] = "Super Duper Important Secret Key"

# login_manager = LoginManager()
# login_manager.init_app(app)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = strg.search(username=request.form['username'])
#         if user and user.check_password(request.form['password']):
#             login_user(user)
#             return 'OK'
#         return 'Invalid username or password'
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     logout_user()
#     return 'OK'

# @login_manager.user_loader
# def load_user(user_id):
#     return strg.search(username=request.form['username'])[0]

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    strg.close()

@app.errorhandler(404)
def error(err):
    return 'oops, nothing here', 404

@app.route('/')
def root():
    return 'hola', 200

# with app.app_context():
#     app.security.datastore.find_or_create_role(
#         name="user", permissions={"user-read", "user-write"}
#     )

#     app.security.datastore.find_or_create_role(
#         name="admin", permissions={"user-read", "user-write", "admin-read", "admin-write"}
#     )
#     strg.save()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

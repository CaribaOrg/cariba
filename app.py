#!/usr/bin/python3

from flask import Flask
from models import strg
from api import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    strg.close()

@app.errorhandler(404)
def error(err):
    return 'oops, nothing here', 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

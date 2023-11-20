#!/usr/bin/python3

from flask import jsonify
from api import api

@api.route('/status')
def status():
    return 'OK', 200

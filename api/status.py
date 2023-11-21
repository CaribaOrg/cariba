#!/usr/bin/python3

from api import api

@api.route('/status')
def status():
    return 'OK', 200

#!/usr/bin/python3

from flask import Blueprint

api = Blueprint('api', __name__)

from api.status import *
from api.user import *

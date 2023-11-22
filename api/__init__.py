#!/usr/bin/python3

from flask import Blueprint
from flask_restx import Api

api = Blueprint('api', __name__)
api_restplus = Api(api)

from api.status import *
from api.user import *
from api.order import *
from api.category import *
from api.part import *
from api.api_swagger import *
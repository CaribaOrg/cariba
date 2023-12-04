#!/usr/bin/python3

from flask import Blueprint
from flask_restx import Api, Namespace

api = Blueprint('api', __name__)
api_restx = Api(api, title="Cariba API", description="An API for the website Cariba", default='Cariba_API', default_label='Endpoint for modifying data in the Cariba website database.')

from api.status import *
from api.user import *
from api.order import *
from api.category import *
from api.part import *
from api.api_swagger import *
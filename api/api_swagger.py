#!/usr/bin/python3
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from models.user import User
from models import strg
from api import api
from flask import jsonify

spec = APISpec(
    title='flask-api-swagger',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin()]
)

@api.route('/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())
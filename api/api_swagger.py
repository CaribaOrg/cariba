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

@api.route('/users', methods=['GET'])
def all_users():
    '''Get list of Users
        ---
        get:
            description: Get list of Users
            response:
                200:
                    description: Return a list
                    content:
                        application/json:
                            schema:
    '''
    users = strg.all(User)
    return jsonify([user.dictify() for user in users])
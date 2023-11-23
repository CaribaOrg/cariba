#!/usr/bin/python3

from flask import jsonify, request
from api import api_restx
from models import strg
from models.product import Product
from flask_restx import Resource, fields

part_model = api_restx.model('Parts', {
    'name': fields.String(required=True, description='Name of the product'),
    'category_id': fields.String(required=True, description='Category ID of the product'),
    'price': fields.Float(required=True, description='Price of the product'),
    'quantity': fields.Integer(required=False, description='Quantity of the product'),
    'description': fields.String(required=False, description='Description of the product'),    'quantity': fields.Integer(required=False, description='Quantity of the product'),
    'rating': fields.Float(required=False, description='Rating of the product'),
})

class Parts(Resource):
    @api_restx.response(200, 'Success')
    def get(self):
        products = strg.all(Product)
        return jsonify([product.dictify() for product in products])
    
    @api_restx.expect(part_model)
    @api_restx.response(200, 'Success')
    @api_restx.response(400, 'Bad Request')
    @api_restx.response(404, 'Not Found')
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        if 'name' not in data or 'price' not in data or 'category_id' not in data:
            return {'error': 'Name, price and category_id are required'}, 404
        ignore_list = ['id', 'created_at', 'updated_at', 'category']
        p_dict = {}
        for key, value in data.items():
            if key not in ignore_list:
                p_dict[key] = value
        part = Product(**p_dict)
        return jsonify(part.dictify())


class Part(Resource):
    @api_restx.response(200, 'Success')
    @api_restx.response(404, 'Not Found')
    def get(self, product_id):
        product = strg.search(cls=Product, id=product_id)
        if not product:
            return 'None found', 404
        part_dict = product.dictify()
        part_dict['category'] = product.category.dictify()
        return jsonify(part_dict)

    @api_restx.expect(part_model)
    @api_restx.response(200, 'Success')
    @api_restx.response(400, 'Bad Request')
    @api_restx.response(404, 'Not Found')
    def put(self, product_id):
        product = strg.search(cls=Product, id=product_id)
        if not product:
           return {'error': 'None found'}, 404
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        ignore_list = ['id', 'created_at', 'updated_at', 'category']
        for key, value in data.items():
            if key not in ignore_list:
                setattr(product, key, value)
        product.save()
        return jsonify(product.dictify())
    
    @api_restx.response(200, 'Success')
    @api_restx.response(404, 'Not Found')
    def delete(self, product_id):
        part = strg.search(cls=Product, id=product_id)
        if not part:
            return {'error': 'None found'}, 404
        part.delete()
        return jsonify({})

api_restx.add_resource(Parts, '/parts')
api_restx.add_resource(Part, '/parts/<product_id>')
#!/usr/bin/python3

from flask import jsonify
from api import api_restplus
from models import strg
from models.product import Product
from flask_restx import Resource

class Parts(Resource):
    def get(self):
        products = strg.all(Product)
        return jsonify([product.dictify() for product in products])


class Part(Resource):
    def get(self, product_id):
        product = strg.search(cls=Product, id=product_id)
        if not product:
            return 'None found', 404
        category_dict = product.dictify()
        return jsonify(product.dictify())


api_restplus.add_resource(Parts, '/parts')
api_restplus.add_resource(Part, '/parts/<product_id>')
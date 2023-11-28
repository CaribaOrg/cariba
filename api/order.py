#!/usr/bin/python3

from flask import jsonify
from api import api_restx
from models import strg
from models.order import Order
from flask_restx import Resource


class Orders(Resource):
    @api_restx.response(200, 'Successful Operation')
    def get(self):
        orders = strg.all(Order)
        return jsonify([order.dictify() for order in orders])


class Orders2(Resource):
    @api_restx.response(200, 'Successful Operation')
    @api_restx.response(404, 'Invalid ID supplied')
    def get(self, order_id):
        order = strg.search(cls=Order, id=order_id)
        if not order:
            return 'None found', 404
        order_dict = order.dictify()
        order_dict.pop('user_id')
        user_dict = order.user.dictify()
        user_dict['shipping_address'] = order.user.address.dictify() if order.user.address else None
        order_dict['user'] = user_dict
        order_dict.pop('cart_id')
        items = []
        for item in order.cart.cart_items:
            item_dict = item.dictify()
            item_dict.pop('cart_id')
            item_dict.pop('product_id')
            prod_dict = {}
            prod_dict['id'] = item.product.id
            prod_dict['name'] = item.product.name
            prod_dict['price'] = item.product.price
            item_dict['product'] = prod_dict
            items.append(item_dict)
        order_dict['items'] = items
        return jsonify(order_dict)
    

api_restx.add_resource(Orders, '/orders')
api_restx.add_resource(Orders2, '/orders/<order_id>')
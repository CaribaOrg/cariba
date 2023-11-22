#!/usr/bin/python3

from flask import jsonify
from api import api_restplus
from models import strg
from models.user import User
from flask_restx import Resource

class Users(Resource):
    def get(self):
        users = strg.all(User)
        return jsonify([user.dictify() for user in users])


class Users2(Resource):
    def get(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        user_dict = user.dictify()
        user_dict['address'] = user.address.dictify() if user.address else None
        user_dict['cars'] = len(user.cars)
        user_dict['orders'] = len(user.orders)
        return jsonify(user_dict)
    
    def delete(self, user_id):
        user = strg.search(cls=User, id=user_id)
        user = user[0] if len(user) > 0 else None
        if not user:
            return 'None found', 404
        user.delete()
        return jsonify({})
        

class UserCart(Resource):
    def get(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        cart_dict = user.cart.dictify()
        items = []
        for item in user.cart.cart_items:
            item_dict = item.dictify()
            item_dict.pop('cart_id')
            item_dict.pop('product_id')
            prod_dict = {}
            prod_dict['id'] = item.product.id
            prod_dict['name'] = item.product.name
            prod_dict['price'] = item.product.price
            item_dict['product'] = prod_dict
            items.append(item_dict)
        cart_dict['items'] = items
        return jsonify(cart_dict)

class UserCheckout(Resource):
    def get(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        order = user.cart.checkout()
        order_dict = order.dictify()
        order_dict.pop('user_id')
        cart_dict = {}
        cart_dict['total_price'] = order.cart.total_price
        cart_dict['total_items'] = order.cart.total_items
        order_dict['cart_info'] = cart_dict
        return jsonify(order_dict)
        

class UserGarage(Resource):
    def get(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        cars_dict = {}
        cars_dict['count'] = len(user.cars)
        cars_list = []
        for car in user.cars:
            cars = car.dictify()
            cars.pop('user_id')
            cars_list.append(cars)
        cars_dict['cars'] = cars_list
        return jsonify(cars_dict)

class UserOrder(Resource):
    def get(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        orders_dict = {}
        orders_dict['count'] = len(user.orders)
        orders_list = []
        for order in user.orders:
            orders = order.dictify()
            orders.pop('user_id')
            orders_list.append(orders)
            cart_dict = {}
            cart_dict['total_price'] = order.cart.total_price
            cart_dict['total_items'] = order.cart.total_items
            orders['cart_info'] = cart_dict
        orders_dict['orders'] = orders_list
        return jsonify(orders_dict)


api_restplus.add_resource(Users, '/users')
api_restplus.add_resource(Users2, '/users/<user_id>')
api_restplus.add_resource(UserCart, '/users/<user_id>/cart')
api_restplus.add_resource(UserGarage, '/users/<user_id>/garage')
api_restplus.add_resource(UserOrder, '/users/<user_id>/orders')
api_restplus.add_resource(UserCheckout, '/users/<user_id>/checkout')

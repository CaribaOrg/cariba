#!/usr/bin/python3

from flask import jsonify
from api import api
from models import strg
from models.user import User
from models.address import Address
from models.cart_item import CartItem

@api.route('/users', methods=['GET'])
def all_users():
    users = strg.all(User)
    return jsonify([user.dictify() for user in users])

@api.route('/users/<user_id>', methods=['GET'])
def user(user_id):
    user = strg.search(cls=User, id=user_id)
    user = user[0] if len(user) > 0 else None
    if not user:
        return 'None found'
    user_dict = user.dictify()
    user_dict['address'] = user.address.dictify()
    user_dict['cars'] = len(user.cars)
    user_dict['orders'] = len(user.orders)
    return jsonify(user_dict)

@api.route('/users/<user_id>/cart', methods=['GET'])
def user_cart(user_id):
    user = strg.search(cls=User, id=user_id)
    user = user[0] if len(user) > 0 else None
    if not user:
        return 'None found'
    cart_dict = user.cart.dictify()
    items = []
    for item in user.cart.cart_items:
        item_dict = item.dictify()
        item_dict.pop('cart_id')
        item_dict.pop('product_id')
        prod_dict = {}
        prod_dict['id'] = item.product.dictify()['id']
        prod_dict['name'] = item.product.dictify()['name']
        prod_dict['price'] = item.product.dictify()['price']
        item_dict['product'] = prod_dict
        items.append(item_dict)
    cart_dict['items'] = items
    return jsonify(cart_dict)

@api.route('/users/<user_id>/garage', methods=['GET'])
def user_cars(user_id):
    user = strg.search(cls=User, id=user_id)
    user = user[0] if len(user) > 0 else None
    if not user:
        return 'None found'
    cars_dict = {}
    cars_dict['count'] = len(user.cars)
    cars_list = []
    for car in user.cars:
        cars = car.dictify()
        cars.pop('user_id')
        cars_list.append(cars)
    cars_dict['cars'] = cars_list
    return jsonify(cars_dict)


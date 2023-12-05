#!/usr/bin/python3

from flask import jsonify, request
from api import api_restx
from models import strg
from models.user import User
from models.car import Car
from flask_restx import Resource, fields

user_model = api_restx.model('User', {
    'username': fields.String(required=True, description='Username of the user'),
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'email': fields.String(required=True, description='email of the user'),
    'active': fields.Boolean(required=False, description='Is the user active?'),
    'role': fields.String(required=False, description='Role', default='user'),
})

class Users(Resource):
    @api_restx.response(200, 'Successful operation')
    def get(self):
        users = strg.all(User)
        return jsonify([user.dictify() for user in users])
    
    @api_restx.expect(user_model)
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(400, 'Invalid Request Format')
    @api_restx.response(404, 'Invalid ID supplied')
    @api_restx.response(409, 'Non unique parameters supplied')
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        if 'username' not in data or 'password' not in data or 'email' not in data:
            return {'error': 'Username, email and password are required'}, 404
        if strg.search(cls=User, username=data['username']):
            return {'error': 'Username is not unique'}, 409
        if strg.search(cls=User, email=data['email']):
            return {'error': 'Email is not unique'}, 409
        ignore_list = ['id', 'created_at', 'updated_at', 'cars', 'cart', 'address', 'orders']
        user_dict = {}
        for key, value in data.items():
            if key not in ignore_list:
                user_dict[key] = value
        user = User(**user_dict)
        return jsonify(user.dictify())


class Users2(Resource):
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(404, 'Invalid ID supplied')
    def get(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        user_dict = user.dictify()
        user_dict['address'] = user.address.dictify() if user.address else None
        user_dict['cars'] = len(user.cars)
        user_dict['orders'] = len(user.orders)
        return jsonify(user_dict)
    
    @api_restx.expect(user_model)
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(400, 'Invalid Request Format')
    @api_restx.response(404, 'Invalid ID supplied')
    @api_restx.response(409, 'Non unique parameters supplied')
    def put(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
           return {'error': 'None found'}, 404
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        ignore_list = ['id', 'created_at', 'updated_at', 'cars', 'cart', 'address', 'orders']
        if 'username' in data.keys() and strg.search(cls=User, username=data['username']):
            return {'error': 'Username is not unique'}, 409
        if 'email' in data.keys() and strg.search(cls=User, email=data['email']):
            return {'error': 'Username is not unique'}, 409
        for key, value in data.items():
            if key not in ignore_list:
                setattr(user, key, value)
        user.save()
        return jsonify(user.dictify())
        
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(404, 'Invalid ID supplied')
    def delete(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        user.delete()
        return jsonify({})
        

class UserCart(Resource):
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(404, 'Invalid ID supplied')
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
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(404, 'Invalid ID supplied')
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
        
car_model = api_restx.model('Car', {
    'name': fields.String(required=True, description='Name of the car'),
    'vin': fields.String(required=True, description='Vehicle Identification Number of the car'),
    'make': fields.String(required=False, description='Make of the car'),
    'model': fields.String(required=False, description='Model of the car'),
    'year': fields.Integer(required=False, description='Year of the car')
})

class UserGarage(Resource):
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(404, 'Invalid ID supplied')
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
    
    @api_restx.expect(car_model)
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(400, 'Invalid Request Format')
    @api_restx.response(404, 'Invalid ID supplied')
    def post(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        if 'vin' not in data or 'name' not in data:
            return {'error': 'Name and VIN are required'}, 404
        ignore_list = ['id', 'created_at', 'updated_at', 'user_id', 'user']
        car_dict = {}
        for key, value in data.items():
            if key not in ignore_list:
                car_dict[key] = value
        car_dict['user_id'] = user.id
        car = Car(**car_dict)
        return jsonify(car.dictify())
    
class GarageUser(Resource):
    @api_restx.expect(car_model)
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(400, 'Invalid Request Format')
    @api_restx.response(404, 'Invalid ID supplied')
    def put(self, user_id, car_id):
        if not strg.search(cls=User, id=user_id):
            return {'error': 'None found'}, 404
        car = strg.search(cls=Car, id=car_id)
        if not car:
           return {'error': 'None found'}, 404
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        ignore_list = ['id', 'created_at', 'updated_at', 'user_id', 'user']
        for key, value in data.items():
            if key not in ignore_list:
                setattr(car, key, value)
        car.save()
        return jsonify(car.dictify())
    
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(404, 'Invalid ID supplied')
    def delete(self, user_id, car_id):
        if not strg.search(cls=User, id=user_id):
            return {'error': 'None found'}, 404
        car = strg.search(cls=Car, id=car_id)
        if not car:
           return {'error': 'None found'}, 404
        car.delete()
        return jsonify({})
        

class UserOrder(Resource):
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(404, 'Invalid ID supplied')
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
    
address_model = api_restx.model('Address', {
    'address': fields.String(required=True, description='Address'),
    'city': fields.String(required=True, description='City'),
    'region': fields.String(required=False, description='Region'),
    'country': fields.String(required=False, description='Country'),
    'zip_code': fields.Integer(required=False, description='Zip coder')
})

class UserAddress(Resource):
    @api_restx.response(200, 'Successful operation')
    def get(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        address_dict = user.address.dictify()
        address_dict.pop('user_id')
        return jsonify(address_dict)
    
    @api_restx.expect(address_model)
    @api_restx.response(200, 'Successful operation')
    def put(self, user_id):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return {'error': 'None found'}, 404
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        ignore_list = ['id', 'created_at', 'updated_at', 'user_id', 'user']
        for key, value in data.items():
            if key not in ignore_list:
                setattr(user.address, key, value)
        user.address.save()
        return jsonify(user.address.dictify())


api_restx.add_resource(Users, '/users')
api_restx.add_resource(Users2, '/users/<user_id>')
api_restx.add_resource(UserCart, '/users/<user_id>/cart')
api_restx.add_resource(UserGarage, '/users/<user_id>/garage')
api_restx.add_resource(GarageUser, '/users/<user_id>/garage/<car_id>')
api_restx.add_resource(UserOrder, '/users/<user_id>/orders')
api_restx.add_resource(UserCheckout, '/users/<user_id>/checkout')
api_restx.add_resource(UserAddress, '/users/<user_id>/address')

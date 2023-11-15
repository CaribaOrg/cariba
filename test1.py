#!/usr/bin/python3

from models.user import User
from models.address import Address
from models.car import Car
from models.base_model import BaseModel, Base
from models import strg

user_dict = {
        'username': 'username1',
        'first_name': 'f_name1',
        'last_name': 'l_name1',
        'password': 'pwd1',
        'email': 'email1'
        }

usr = User(**user_dict)
usr.save()

print('------------User:')
print(usr.__dict__)
address_dict = {
        'street':'strt1',
        'city': 'city1',
        'state_province': 'st1',
        'zip_code': 123,
        'country': 'cntr1',
        'user_id': usr.id
        }

address = Address(**address_dict)
address.save()


print('------------Address:')
print(address.__dict__)

car_dict = {
        'user_id': usr.id,
        'vin': 123
        }
car = Car(**car_dict)
car.save()
print('------------Car:')
print(car.__dict__)
print(car.user.id)

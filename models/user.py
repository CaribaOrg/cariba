#!/usr/bin/python3
''' This is a module for User '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields



class User(BaseModel, Base):
    '''
    User class represents a registered user.

    Attributes:
        username (str): The username of the user (unique).
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        password (str): The hashed password of the user.
        email (str): The email address of the user (unique).
        address (relationship): The relationship with the associated address.
        cart (relationship): The relationship with associated shopping cart.
        cars (relationship): The relationship with associated cars.
        orders (relationship): The relationship with associated orders.
        role (str): The role of the user (default='user').

    Relationships:
        - 'address': Represents the associated address.
        - 'cart': Represents the associated shopping cart.
        - 'cars': Represents associated cars with cascade delete.
        - 'orders': Represents associated orders with cascade delete.

    '''
    __tablename__ = 'users'
    username = Column(String(128))
    first_name = Column(String(128))
    last_name = Column(String(128))
    password = Column(String(128))
    email = Column(String(128))
    address = relationship('Address',
                           uselist=False,
                           back_populates='user',
                           cascade='all, delete-orphan')
    cart = relationship('Cart',
                        uselist=False,
                        back_populates='user')
    cars = relationship('Car',
                        back_populates='user',
                        cascade='all, delete-orphan')
    orders = relationship('Order',
                          back_populates='user',
                          cascade='all, delete-orphan')
    role = Column(String(10), default='user')

    def __init__(self, **kwargs):
        from models.cart import Cart
        '''
        Initialize a new instance of the User class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)
        cart_dict = {'user_id': self.id}
        crt = Cart(**cart_dict)
        crt.save()

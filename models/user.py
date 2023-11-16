#!/usr/bin/python3
''' This is a module for User '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


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
    username = Column(String(128), nullable=False, unique=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    address = relationship('Address',
                           uselist=False,
                           back_populates='user',
                           cascade='all, delete-orphan')
    cart = relationship('Cart',
                        uselist=False,
                        back_populates='user',
                        cascade='all, delete-orphan')
    cars = relationship('Car',
                        back_populates='user',
                        cascade='all, delete-orphan')
    orders = relationship('Order',
                          back_populates='user',
                          cascade='all, delete-orphan')
    role = Column(String(10), default='user')

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the User class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

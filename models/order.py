#!/usr/bin/python3
''' This is a module for Order '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
import random


class Order(BaseModel, Base):
    '''
    Order class represents a user's order.

    Attributes:
        user_id (str): The foreign key referencing the associated user.
        user (relationship): The relationship with the associated user.
        order_status (str): The status of the order.
        cart_id (str): The foreign key referencing the associated cart.
        cart (relationship): The relationship with the associated cart.

    Relationships:
        - 'user': Represents the associated user with a back-ref to 'orders'.
        - 'cart': Represents the associated cart.
    '''
    __tablename__ = 'orders'
    user_id = Column(String(128), ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
    order_status = Column(String(128))
    cart_id = Column(String(128), ForeignKey('carts.id'))
    cart = relationship('Cart')

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Order class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

#!/usr/bin/python3
''' This is a module for Cart '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class Cart(BaseModel, Base):
    '''
    Cart class represents a shopping cart associated with a user.

    Attributes:
        user_id (str): The foreign key referencing the associated user.
        user (relationship): The relationship with the associated user.
        total_price (float): The total price of items in the cart.
        cart_items (relationship): The relationship with associated cart items.

    Relationships:
        - 'user': Represents the linked user with a back-reference to 'cart'.
        - 'cart_items': Represents the linked cart items with cascade delete.
    '''
    __tablename__ = 'carts'
    user_id = Column(String(128), ForeignKey('users.id'))
    user = relationship('User', back_populates='cart')
    total_price = Column(Float, default=0)
    total_items = Column(Integer, default=0)
    cart_items = relationship('CartItem',
                              back_populates='cart',
                              cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Cart class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

    def checkout(self):
        '''
        Checkout the items in the cart, creating an order and
        resetting the cart.

        Returns:
            Order: The order created during the checkout process.
        '''
        from models.order import Order
        order_dict = {
                'user_id': self.user_id,
                'cart_id': self.id
                }
        order = Order(**order_dict)
        order.save()
        self.user_id = None
        return order

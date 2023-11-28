#!/usr/bin/python3
''' This is a module for CartItem '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class CartItem(BaseModel, Base):
    '''
    CartItem class represents an item in a shopping cart.

    Attributes:
        cart_id (str): The foreign key referencing the associated cart.
        cart (relationship): The relationship with the associated cart.
        quantity (int): The quantity of the product in the cart.
        product_id (str): The foreign key referencing the associated product.
        product (relationship): The relationship with the associated product.

    Relationships:
        - 'cart': Represents the associated cart with back-ref to 'cart_items'.
        - 'product': Represents the associated product.
    '''
    __tablename__ = 'cart_items'
    cart_id = Column(String(128), ForeignKey('carts.id'), nullable=False)
    cart = relationship('Cart', back_populates='cart_items')
    quantity = Column(Integer)
    product_id = Column(String(128), ForeignKey('products.id'))
    product = relationship('Product')

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the CartItem class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

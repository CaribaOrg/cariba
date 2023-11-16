#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import requests
import json

class CartItem(BaseModel, Base):
    __tablename__ = 'cart_items'
    cart_id = Column(String(128), ForeignKey('carts.id'), nullable=False)
    cart = relationship('Cart', back_populates='cart_items')
    quantity = Column(Integer)
    product_id = Column(String(128), ForeignKey('products.id'))
    product = relationship('Product')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

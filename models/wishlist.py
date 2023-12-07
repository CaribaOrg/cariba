#!/usr/bin/python3
''' This is a module for CartItem '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship


class WishlistItem(BaseModel, Base):
    __tablename__ = 'wishlist_items'
    product_id = Column(String(60), ForeignKey('products.id'))
    product = relationship('Product')
    user_id = Column(String(60), ForeignKey('users.id'))
    user = relationship('User', back_populates='wishlist_items')
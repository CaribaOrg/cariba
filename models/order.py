#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

class Order(BaseModel, Base):
    __tablename__ = 'orders'
    user_id = Column(String(128), ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
    order_status = Column(String(128))
    cart_id = Column(String(128), ForeignKey('carts.id'))
    cart = relationship('Cart')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

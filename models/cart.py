#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

class Cart(BaseModel, Base):
    __tablename__ = 'carts'
    user_id = Column(String(128), ForeignKey('users.id'))
    user = relationship('User', back_populates='cart')
    total_price = Column(Float, default=0)
    cart_items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def checkout(self):
        from models.order import Order
        order_dict = {
                'user_id': self.user_id,
                'cart_id': self.id
                }
        order = Order(**order_dict)
        order.save()
        self.user_id = None
        return order

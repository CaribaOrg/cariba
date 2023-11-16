#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship

class Product(BaseModel, Base):
    __tablename__ = 'products'
    name = Column(String(128))
    price = Column(Float, default=0)
    description = Column(String(1024))
    quantity = Column(Integer, default=1)
    oem_number = Column(String(128))
    category_id = Column(String(60), ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products', uselist=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_to_cart(self, user, quantity=1):
        from models.cart_item import CartItem
        for item in user.cart.cart_items:
            if self.id == item.product.id:
                if quantity <= 0 or quantity + item.quantity > self.quantity:
                    quantity = self.quantity - item.quantity
                item.quantity += quantity
                return
        if quantity <= 0 or quantity > self.quantity:
            quantity = self.quantity
        ci_dict = {
                'cart_id': user.cart.id,
                'product_id': self.id,
                'quantity': quantity
                }
        ci = CartItem(**ci_dict)
        ci.save()
        user.cart.cart_items.append(ci)

#!/usr/bin/python3
''' This is a module for Product '''

import random
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    '''
    Product class represents a product in the inventory.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product (default=0).
        description (str): The description of the product.
        quantity (int): The quantity available in the inventory (default=1).
        oem_number (str): The Original Equipment Manufacturer (OEM)
            number of the product.
        category_id (str): The foreign key referencing the associated category.
        category (relationship): The relationship with the associated category.

    Relationships:
        - 'category': Represents the linked category, back-ref to 'products'.
    '''
    __tablename__ = 'products'
    name = Column(String(1024))
    price = Column(Float, default=0)
    description = Column(String(1024))
    quantity = Column(Integer, default=1)
    rating = Column(Float)
    category_id = Column(String(60), ForeignKey('categories.id'))
    category = relationship('Category',
                            back_populates='products',
                            uselist=False)

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Product class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)
        self.rating = round(random.uniform(3.0, 5.0), 1)
        self.quantity = round(random.uniform(0, 500))

    def add_to_cart(self, user, quantity=1):
        '''
        Add the product to the user's shopping cart.

        Args:
            user (User): The user for whom the product is added to the cart.
            quantity (int): The quantity of product to be added (default=1).
        '''
        from models.cart_item import CartItem
        for item in user.cart.cart_items:
            if self.id == item.product.id:
                if quantity <= 0 or quantity + item.quantity > self.quantity:
                    quantity = self.quantity - item.quantity
                item.quantity += quantity
                item.cart.total_price += quantity * self.price
                item.cart.total_items += quantity
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
        user.cart.total_price += quantity * self.price
        user.cart.total_items += quantity
        user.save()
        print('quantity:', quantity)
        print('total_items:', user.cart.total_items)

    def remove_from_cart(self, user, quantity=1):
        '''
        Remove a specified quantity of the product from user's shopping cart.

        Args:
            user (User): The user whose cart needs to be updated.
            quantity (int, optional): The quantity of the product to be removed
                (default=1).
        '''
        from models.cart_item import CartItem
        for item in user.cart.cart_items:
            if self.id == item.product.id:
                if item.quantity <= quantity:
                    item.delete()
                    user.cart.cart_items.remove(item)
                    user.cart.total_price -= item.quantity * self.price
                    user.cart.total_items -= item.quantity
                    user.save()
                    return
                user.cart.total_price -= self.price * quantity
                item.quantity -= quantity
                item.cart.total_items -= quantity
                item.save()
                user.save()
                return

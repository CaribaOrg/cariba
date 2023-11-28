#!/usr/bin/python3
"""Unittests for models/engin/storage.py.

Unittest classes:
    TestStorageModel
=============================================
==> Make sure the cariba_test_db is empty <==
=============================================
"""
import os
import unittest
from datetime import datetime
from time import sleep
import models
from models.base_model import BaseModel, Base
from models.user import User
from models.address import Address
from models.car import Car
from models.cart import Cart
from models.cart_item import CartItem
from models.category import Category
from models.product import Product
from models.order import Order
from os import getenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class TestStorageModel(unittest.TestCase):
    """Stroage testcases"""
    @classmethod
    def setUpClass(cls):
        engine = create_engine('mysql://cariba_test:cariba123@localhost/cariba_test_db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        clsList = [User, Address, Car, Cart, CartItem, Category, Product, Order]
        [session.query(mdl).delete() for mdl in clsList]
        session.commit()
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        cls.user = User(username="flan_10",
                         first_name="Folan",
                         last_name="Fortlan",
                         password="123456")
        cls.address = Address(user_id=cls.user.id,
                               street="back street",
                               city="Nairobi",
                               state_province="Nairobi",
                               zip_code=1247)
        cls.car = Car(user_id=cls.user.id,
                       vin="5UXWX9C50E0D42624",
                       name="MyCar",
                       make="Honda",
                       model="Accord",
                      year=2022)
        cls.category = Category(name="Interior Accessories",
                                 description="Interior accessories")
        cls.product = Product(name="Floor mat",
                               price=5.99,
                               quantity=100,
                               oem_number="99061",
                               category_id=cls.category.id)
        cls.order = Order(user_id=cls.user.id,
                           order_status="Pending",
                           cart_id=cls.user.cart.id)
        cls.cartItem = CartItem(cart_id=cls.user.cart.id,
                                 quantity=1,
                                 product_id=cls.product.id)

    def test_all_returns_list(self):
        self.assertIs(type(models.strg.all()), list)

    def test_all_no_arg_class(self):
        self.assertTrue(len(models.strg.all()) == 8)

    def test_all_user_class(self):
        self.assertTrue(len(models.strg.all(User)) == 1)

    def test_all_car_class(self):
        self.assertTrue(len(models.strg.all(Car)) == 1)

    def test_all_cart_class(self):
        self.assertTrue(len(models.strg.all(Cart)) == 1)

    def test_all_category_class(self):
        self.assertTrue(len(models.strg.all(Category)) == 1)

    def test_all_cart_item_class(self):
        self.assertTrue(len(models.strg.all(CartItem)) == 1)

    def test_all_product_class(self):
        self.assertTrue(len(models.strg.all(Product)) == 1)

    def test_all_order_class(self):
        self.assertTrue(len(models.strg.all(Order)) == 1)

    def test_all_address_class(self):
        self.assertTrue(len(models.strg.all(Address)) == 1)

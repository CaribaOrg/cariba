#!/usr/bin/python3
"""Unittests for models/cart.py.

Unittest classes:
    TestCartModel
"""
import os
import time
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.user import User
from models.cart import Cart


class TestCartModel(unittest.TestCase):
    """Testing instantiating of the cart model class."""

    def setUp(self):
        self.user1 = User()
        self.user2 = User()
        self.cart = Cart(user_id=self.user1.id)
        self.cart2 = Cart(user_id=self.user2.id)

    def test_is_subclass_of_basemodel(self):
        self.assertIsInstance(self.cart, BaseModel)
        self.assertTrue(hasattr(self.cart, "id"))
        self.assertTrue(hasattr(self.cart, "created_at"))
        self.assertTrue(hasattr(self.cart, "updated_at"))

    def test_id_is_str(self):
        self.assertEqual(str, type(self.cart.id))

    def test_create_at_is_datetime(self):
        self.assertEqual(datetime, type(self.cart.created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(self.cart.updated_at))

    def test_user_id_attr(self):
        self.assertTrue(hasattr(self.cart, "user_id"))
        self.assertEqual(self.cart.user_id, self.user1.id)

    def test_total_price_attr(self):
        self.assertTrue(hasattr(self.cart, "total_price"))
        self.assertEqual(self.cart.total_price, 0)

    def test_total_items_attr(self):
        self.assertTrue(hasattr(self.cart, "total_items"))
        self.assertEqual(self.cart.total_items, 0)

    def test_cart_items_attr(self):
        self.assertTrue(hasattr(self.cart, "cart_items"))
        self.assertEqual(self.cart.cart_items, [])

    def test_two_models_unique_id(self):
        self.assertTrue(self.cart.id != self.cart2.id)

    def test_save_method(self):
        obj_id = self.cart.id
        self.cart.total_price = 100
        self.assertEqual(self.cart.id, obj_id)
        self.assertTrue(self.cart.total_price == 100)

    def test_update_at_updated(self):
        old_date = self.cart.updated_at
        time.sleep(1)
        self.cart.total_items = 2
        self.cart.save()
        self.assertTrue(old_date < self.cart.updated_at)

    def test_delete_method(self):
        from models import strg

        self.cart2.delete()
        all_obj = strg.all(Cart)
        self.assertTrue(self.cart2 not in all_obj)

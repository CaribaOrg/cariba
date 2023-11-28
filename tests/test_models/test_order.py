#!/usr/bin/python3
"""Unittests for models/order.py.

Unittest classes:
    TestOrderModel
"""
import os
import time
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.user import User
from models.order import Order


class TestOrderModel(unittest.TestCase):
    """Testing instantiating of the order model class."""

    def setUp(self):
        self.user = User()
        self.order1 = Order(user_id=self.user.id)
        self.order2 = Order(user_id=self.user.id)

    def test_is_subclass_of_basemodel(self):
        self.assertIsInstance(self.order1, BaseModel)
        self.assertTrue(hasattr(self.order1, "id"))
        self.assertTrue(hasattr(self.order1, "created_at"))
        self.assertTrue(hasattr(self.order1, "updated_at"))

    def test_instantiate_no_args(self):
        self.assertEqual(Order, type(self.order1))

    def test_id_is_str(self):
        self.assertEqual(str, type(self.order1.id))

    def test_create_at_is_datetime(self):
        self.assertEqual(datetime, type(self.order1.created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(self.order1.updated_at))

    def test_user_id_attr(self):
        self.assertTrue(hasattr(self.order1, "user_id"))
        self.assertEqual(self.order1.user_id, self.user.id)

    def test_order_status_attr(self):
        self.assertTrue(hasattr(self.order1, "order_status"))
        self.assertEqual(self.order1.order_status, None)

    def test_cart_id_attr(self):
        self.assertTrue(hasattr(self.order1, "cart_id"))
        self.assertEqual(self.order1.cart_id, None)

    def test_two_models_unique_id(self):
        self.assertTrue(self.order1.id != self.order2.id)

    def test_save_method(self):
        obj1 = User(username="quelqueen")
        obj_id = obj1.id
        obj1.username = "newName_lol"
        self.assertEqual(obj1.id, obj_id)
        self.assertTrue(obj1.username != "quelqueen")

    def test_update_at_updated(self):
        old_date = self.order1.updated_at
        time.sleep(1)
        self.order1.order_status = "Pending"
        self.order1.save()
        self.assertTrue(old_date < self.order1.updated_at)

    def test_delete_method(self):
        from models import strg

        self.order2.delete()
        all_obj = strg.all(Order)
        self.assertTrue(self.order2 not in all_obj)

#!/usr/bin/python3
"""Unittests for models/cart_item.py.

Unittest classes:
    TestCartItemModel
"""
import os
import time
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.cart_item import CartItem
from models.cart import Cart


class TestCartItemModel(unittest.TestCase):
    """Testing instantiating of the product model class."""

    def setUp(self):
        self.cart = Cart()
        self.cart_item = CartItem(cart_id=self.cart.id)
        self.cart_item2 = CartItem(cart_id=self.cart.id)

    def test_is_subclass_of_basemodel(self):
        self.assertIsInstance(self.cart_item, BaseModel)
        self.assertTrue(hasattr(self.cart_item, "id"))
        self.assertTrue(hasattr(self.cart_item, "created_at"))
        self.assertTrue(hasattr(self.cart_item, "updated_at"))

    def test_instantiate_no_args(self):
        self.assertEqual(CartItem, type(self.cart_item))

    def test_id_is_str(self):
        self.assertEqual(str, type(self.cart_item.id))

    def test_create_at_is_datetime(self):
        self.assertEqual(datetime, type(self.cart_item.created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(self.cart_item.updated_at))

    def test_cart_id_attr(self):
        self.assertTrue(hasattr(self.cart_item, "cart_id"))
        self.assertEqual(self.cart_item.cart_id, self.cart.id)

    def test_cart_attr(self):
        self.assertTrue(hasattr(self.cart_item, "cart"))
        self.assertEqual(self.cart_item.cart, self.cart)

    def test_quantity_attr(self):
        self.assertTrue(hasattr(self.cart_item, "quantity"))
        self.assertEqual(self.cart_item.quantity, None)

    def test_product_id_attr(self):
        self.assertTrue(hasattr(self.cart_item, "product_id"))
        self.assertEqual(self.cart_item.product_id, None)

    def test_product_attr(self):
        self.assertTrue(hasattr(self.cart_item, "product"))
        self.assertEqual(self.cart_item.product, None)

    def test_two_models_unique_id(self):
        self.assertTrue(self.cart_item.id != self.cart_item2.id)

    def test_save_method(self):
        obj_id = self.cart_item.id
        self.cart_item.quantity = 2
        self.assertEqual(self.cart_item.id, obj_id)
        self.assertTrue(self.cart_item.quantity != None)

    def test_update_at_updated(self):
        old_date = self.cart_item.updated_at
        time.sleep(1)
        self.cart_item.quantity = 5
        self.cart_item.save()
        self.assertTrue(old_date < self.cart_item.updated_at)

    def test_delete_method(self):
        from models import strg

        self.cart_item2.delete()
        all_obj = strg.all(CartItem)
        self.assertTrue(self.cart_item2 not in all_obj)

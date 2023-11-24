#!/usr/bin/python3
"""Unittests for models/product.py.

Unittest classes:
    TestProductModel
"""
import os
import time
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.product import Product



class TestProductModel(unittest.TestCase):
    """Testing instantiating of the product model class."""

    def setUp(self):
        self.product = Product()
        self.product2 = Product()

    def test_is_subclass_of_basemodel(self):
        self.assertIsInstance(self.product, BaseModel)
        self.assertTrue(hasattr(self.product, "id"))
        self.assertTrue(hasattr(self.product, "created_at"))
        self.assertTrue(hasattr(self.product, "updated_at"))

    def test_instantiate_no_args(self):
        self.assertEqual(Product, type(self.product))

    def test_id_is_str(self):
        self.assertEqual(str, type(self.product.id))

    def test_create_at_is_datetime(self):
        self.assertEqual(datetime, type(self.product.created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(self.product.updated_at))

    def test_name_attr(self):
        self.assertTrue(hasattr(self.product, "name"))
        self.assertEqual(self.product.name, None)

    def test_price_attr(self):
        self.assertTrue(hasattr(self.product, "price"))
        self.assertEqual(self.product.price, 0)

    def test_description_attr(self):
        self.assertTrue(hasattr(self.product, "description"))
        self.assertEqual(self.product.description, None)

    def test_quantity_attr(self):
        self.assertTrue(hasattr(self.product, "quantity"))
        self.assertEqual(self.product.quantity, 1)

    def test_oem_number_attr(self):
        self.assertTrue(hasattr(self.product, "oem_number"))
        self.assertEqual(self.product.oem_number, None)

    def test_category_id_attr(self):
        self.assertTrue(hasattr(self.product, "category_id"))
        self.assertEqual(self.product.category_id, None)

    def test_two_models_unique_id(self):
        self.assertTrue(self.product.id != self.product2.id)

    def test_save_method(self):
        obj_id = self.product.id
        self.product.name = "newproduct"
        self.assertEqual(self.product.id, obj_id)
        self.assertTrue(self.product.name != None)

    def test_update_at_updated(self):
        old_date = self.product.updated_at
        time.sleep(1)
        self.product.name = "another_name"
        self.product.save()
        self.assertTrue(old_date < self.product.updated_at)

    def test_delete_method(self):
        from models import strg

        self.product2.delete()
        all_obj = strg.all(Product)
        self.assertTrue(self.product2 not in all_obj)

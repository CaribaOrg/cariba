#!/usr/bin/python3
"""Unittests for models/category.py.

Unittest classes:
    TestCategoryModel_instantiation
"""
import os
import time
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.category import Category
from hashlib import md5
import re


class TestUserModel(unittest.TestCase):
    """Testing instantiating of the category model class."""

    def test_is_subclass_of_basemodel(self):
        category = Category(name="")
        self.assertIsInstance(category, Category)
        self.assertTrue(hasattr(category, "id"))
        self.assertTrue(hasattr(category, "created_at"))
        self.assertTrue(hasattr(category, "updated_at"))

    def test_instantiate_no_args(self):
        self.assertEqual(Category, type(Category(name="")))

    def test_id_is_str(self):
        self.assertEqual(str, type(Category(name="").id))

    def test_create_at_is_datetime(self):
        self.assertEqual(datetime, type(Category(name="").created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(Category(name="").updated_at))

    def test_name_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "name"))
        self.assertEqual(category.name, "")

    def test_parent_id_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "parent_id"))
        self.assertEqual(category.parent_id, None)

    def test_description_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "description"))
        self.assertEqual(category.description, None)

    def test_active_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "active"))
        self.assertEqual(category.active, True)

    def test_icon_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "icon"))
        self.assertEqual(category.icon, None)

    def test_children_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "children"))
        self.assertEqual(category.children, [])

    def test_parent_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "parent"))

    def test_products_attr(self):
        category = Category(name="")
        self.assertTrue(hasattr(category, "products"))
        self.assertEqual(category.products, [])

    def test_two_models_unique_id(self):
        obj1 = Category(name="")
        obj2 = Category(name="")
        self.assertTrue(obj1.id != obj2.id)

    def test_two_models_diffrent_create_at(self):
        obj1 = Category(name="")
        time.sleep(1)
        obj2 = Category(name="")
        self.assertTrue(obj1.created_at < obj2.created_at)

    def test_save_method(self):
        obj1 = Category(name="")
        obj_id = obj1.id
        obj1.username = "newcategory_lol"
        self.assertEqual(obj1.id, obj_id)
        self.assertTrue(obj1.username != "")

    def test_update_at_updated(self):
        obj1 = Category(name="")
        old_date = obj1.updated_at
        time.sleep(1)
        obj1.name = "another_category"
        obj1.save()
        self.assertTrue(old_date < obj1.updated_at)

    def test_delete_method(self):
        from models import strg

        obj1 = Category(name="")
        obj1.delete()
        all_obj = strg.all(Category)
        self.assertTrue(obj1 not in all_obj)

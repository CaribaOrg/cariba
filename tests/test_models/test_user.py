#!/usr/bin/python3
"""Unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_delete
    TestBaseModel_to_dict
"""
import os
import time
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.user import User
from hashlib import md5
import re


class TestUserModel(unittest.TestCase):
    """Testing instantiating of the user model class."""

    def test_is_subclass_of_basemodel(self):
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_instantiate_no_args(self):
        self.assertEqual(User, type(User()))

    def test_id_is_str(self):
        self.assertEqual(str, type(User().id))

    def test_create_at_is_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_username_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "username"))
        self.assertEqual(user.username, None)

    def test_first_name_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        self.assertEqual(user.first_name, None)

    def test_last_name_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        self.assertEqual(user.last_name, None)

    def test_password_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "password"))
        self.assertEqual(user.password, None)

    def test_email_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertEqual(user.email, None)

    def test_address_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "address"))
        self.assertEqual(user.address, None)

    def test_cart_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "cart"))

    def test_cars_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "cars"))
        self.assertEqual(user.cars, [])

    def test_orders_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "orders"))
        self.assertEqual(user.orders, [])

    def test_role_attr(self):
        user = User()
        self.assertTrue(hasattr(user, "role"))
        self.assertEqual(user.role, "user")

    def test_two_models_unique_id(self):
        obj1 = User(username="john", first_name="doe")
        obj2 = User(username="someone", first_name="someonov")
        self.assertTrue(obj1.id != obj2.id)

    def test_two_models_diffrent_create_at(self):
        obj1 = User(username="martin", first_name="matin")
        obj2 = User(username="admin", first_name="admin", role="admin")
        self.assertTrue(obj1.created_at < obj2.created_at)

    def test_password_is_md5(self):
        obj1 = User(username="quelqueen", password="mypassword")
        """get the pattern of the password"""
        md5_pattern = re.compile(r"^[a-fA-F0-9]{32}$")
        self.assertTrue(md5_pattern.match(obj1.password))

    def test_save_method(self):
        obj1 = User(username="quelqueen")
        obj_id = obj1.id
        obj1.username = "newName_lol"
        self.assertEqual(obj1.id, obj_id)
        self.assertTrue(obj1.username != "quelqueen")

    def test_update_at_updated(self):
        obj1 = User(username="quelqueen")
        old_date = obj1.updated_at
        time.sleep(1)
        obj1.username = "another_name"
        obj1.save()
        self.assertTrue(old_date < obj1.updated_at)

    def test_delete_method(self):
        from models import strg

        obj1 = User(username="quelqueen")
        obj1.delete()
        all_obj = strg.all(User)
        self.assertTrue(obj1 not in all_obj)

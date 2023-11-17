#!/usr/bin/python3
"""Unittests for models/address.py.

Unittest classes:
    TestBaseModel_instantiation
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.address import Address
from hashlib import md5
import re


class TestAddressModel(unittest.TestCase):
    """Testing instantiating of the address model class."""

    def test_is_subclass_of_basemodel(self):
        address = Address(street="", city="",state_province="", zip_code=1)
        self.assertIsInstance(address, Address)
        self.assertTrue(hasattr(address, "id"))
        self.assertTrue(hasattr(address, "created_at"))
        self.assertTrue(hasattr(address, "updated_at"))

    def test_instantiate_no_args(self):
        address = Address(street="", city="",state_province="", zip_code=22)
        self.assertEqual(Address, type(address))

    def test_id_is_str(self):
        address = Address(street="", city="",state_province="", zip_code=2)
        self.assertEqual(str, type(address.id))

    def test_create_at_is_datetime(self):
        address = Address(street="", city="",state_province="", zip_code=2)
        self.assertEqual(datetime, type(address.created_at))

    def test_updated_at_is_datetime(self):
        address = Address(street="", city="",state_province="", zip_code=2)
        self.assertEqual(datetime, type(address.updated_at))

    def test_user_id_attr(self):
        address = Address(street="", city="",state_province="", zip_code=2)
        self.assertTrue(hasattr(address, "user_id"))

    def test_street_attr(self):
        address = Address(street="", city="",state_province="", zip_code=3)
        self.assertTrue(hasattr(address, "street"))
        self.assertEqual(address.street, "")

    def test_city_attr(self):
        address = Address(street="", city="",state_province="", zip_code=4)
        self.assertTrue(hasattr(address, "city"))
        self.assertEqual(address.city, "")

    def test_state_province_attr(self):
        address = Address(street="", city="",state_province="", zip_code=5)
        self.assertTrue(hasattr(address, "state_province"))
        self.assertEqual(address.state_province, "")

    def test_zip_code_attr(self):
        address = Address(street="", city="",state_province="", zip_code=6)
        self.assertTrue(hasattr(address, "zip_code"))
        self.assertEqual(address.zip_code, 6)

    def test_two_models_unique_id(self):
        obj1 = Address(street="", city="",state_province="", zip_code=2)
        obj2 = Address(street="", city="",state_province="", zip_code=2)
        self.assertTrue(obj1.id != obj2.id)

    def test_two_models_diffrent_create_at(self):
        obj1 = Address(street="", city="",state_province="", zip_code=2)
        obj2 = Address(street="", city="",state_province="", zip_code=2)
        self.assertTrue(obj1.created_at < obj2.created_at)

    def test_save_method(self):
        obj1 = Address(street="", city="",state_province="", zip_code=2)
        obj_id = obj1.id
        obj1.street = "back street doesn't exist"
        self.assertEqual(obj1.id, obj_id)
        self.assertTrue(obj1.street != "")

    def test_update_at_updated(self):
        obj1 = Address(street="", city="",state_province="", zip_code=2)
        old_date = obj1.updated_at
        obj1.city = "Nairobi"
        obj1.save()
        self.assertTrue(old_date < obj1.updated_at)

    def test_delete_method(self):
        from models import strg

        obj1 = Address(street="", city="",state_province="", zip_code=2)
        obj1.delete()
        all_obj = strg.all(Address)
        self.assertTrue(obj1 not in all_obj)

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
from models.car import Car
from models.user import User
from hashlib import md5
import re


class TestCarModel(unittest.TestCase):
    """Testing instantiating of the car model class."""

    def setUp(self):
        self.user1 = User()

    def test_is_subclass_of_basemodel(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertIsInstance(car, Car)
        self.assertTrue(hasattr(car, "id"))
        self.assertTrue(hasattr(car, "created_at"))
        self.assertTrue(hasattr(car, "updated_at"))

    def test_instantiate_no_args(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertEqual(Car, type(car))

    def test_id_is_str(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertEqual(str, type(car.id))

    def test_create_at_is_datetime(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertEqual(datetime, type(car.created_at))

    def test_updated_at_is_datetime(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertEqual(datetime, type(car.updated_at))

    def test_name_attr(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertTrue(hasattr(car, "name"))
        self.assertEqual(car.name, None)

    def test_make_attr(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertTrue(hasattr(car, "make"))
        self.assertEqual(car.make, None)

    def test_model_attr(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertTrue(hasattr(car, "model"))
        self.assertEqual(car.model, None)

    def test_year_attr(self):
        car = Car(user_id=self.user1.id, vin="")
        self.assertTrue(hasattr(car, "year"))
        self.assertEqual(car.year, None)

    def test_two_models_unique_id(self):
        obj1 = Car(user_id=self.user1.id, vin="")
        obj2 = Car(user_id=self.user1.id, vin="")
        self.assertTrue(obj1.id != obj2.id)

    def test_two_models_diffrent_create_at(self):
        obj1 = Car(user_id=self.user1.id, vin="")
        obj2 = Car(user_id=self.user1.id, vin="")
        self.assertTrue(obj1.created_at < obj2.created_at)

    def test_save_method(self):
        obj1 = Car(user_id=self.user1.id, vin="")
        obj_id = obj1.id
        obj1.vin = "465-5d"
        obj1.save()
        self.assertEqual(obj1.id, obj_id)
        self.assertTrue(obj1.vin != "")

    def test_update_at_updated(self):
        obj1 = Car(user_id=self.user1.id, vin="")
        old_date = obj1.updated_at
        time.sleep(1)
        obj1.year = 2019
        obj1.save()
        self.assertTrue(old_date < obj1.updated_at)

    def test_delete_method(self):
        from models import strg

        obj1 = Car(user_id=self.user1.id, vin="")
        obj1.delete()
        all_obj = strg.all(Car)
        self.assertTrue(obj1 not in all_obj)

#!/usr/bin/python3
"""Unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_delete
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Testing instantiating of the base model class."""

    def test_instantiate_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_id_is_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_create_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_id(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotTrue(obj1.id, obj2.id)

    def test_two_models_diffrent_create_at(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertTrue(obj1.created_at < obj2.created_at)

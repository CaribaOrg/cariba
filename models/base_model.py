#!/usr/bin/python3
''' This is a module for Base and BaseModel '''

from datetime import datetime
from typing import Any
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
import models
import uuid

time = "%Y-%m-%dT%H:%M:%S"
Base = declarative_base()


class BaseModel:
    '''
    BaseModel class represents the base model for other classes.

    Attributes:
        id (str): The unique identifier for the instance.
        created_at (datetime): The datetime when the instance is created.
        updated_at (datetime): The datetime when the instance is updated.
    '''
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        '''
        Initializes a new instance of the BaseModel.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def __setattr__(self, name, value):
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
        
    def save(self):
        ''' Save the current instance to the storage db. '''
        from models import strg
        self.updated_at = datetime.utcnow()
        strg.new(self)
        strg.save()

    def delete(self):
        ''' Delete the current instance from the storage db. '''
        from models import strg
        strg.delete(self)

    def dictify(self):
        dictified = self.__dict__.copy()
        dictified["created_at"] = dictified["created_at"].strftime(time)
        dictified["updated_at"] = dictified["updated_at"].strftime(time)
        dictified.pop('_sa_instance_state', None)
        dictified.pop('password', None)
        return dictified

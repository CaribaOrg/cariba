#!/usr/bin/python3
''' This is a module for Base and BaseModel '''

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
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
        dictified.pop("created_at", None)
        dictified.pop("updated_at", None)
        dictified.pop('_sa_instance_state', None)
        dictified.pop('password', None)
        return dictified

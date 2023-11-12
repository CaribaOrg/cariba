#!/usr/bin/python3

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
import models
import uuid

time = "%Y-%m-%dT%H:%M:%S"
Base = declarative_base()


class BaseModel:
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    ignore = ["id", "created_at", "updated_at", "__class__"]

    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        print(self.id)
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key not in self.ignore:
                if key == "password":
                    value = md5(value.encode()).hexdigest()
                setattr(self, key, value)

    def save(self):
        from models import strg
        self.updated_at = datetime.utcnow()
        strg.new(self)
        strg.save()

    def delete(self):
        from models import strg
        strg.delete()


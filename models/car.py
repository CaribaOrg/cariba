#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Car(BaseModel, Base):
    __tablename__ = 'cars'
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='cars')
    vin = Column(String(128), nullable=False)
    name = Column(String(128))
    make = Column(String(128))
    model = Column(String(128))
    year = Column(Integer)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import requests
import json

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
        if self.vin:
            url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{}?format=json'.format(self.vin)
            response = requests.get(url).json().get('Results')[0]
            self.make = response.get('Make')
            self.model = response.get('Model')
            self.year = int(response.get('ModelYear'))

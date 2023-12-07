#!/usr/bin/python3
''' This is a module for Car '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import requests
import json


class Car(BaseModel, Base):
    '''
    Car class represents a user's vehicle.

    Attributes:
        user_id (str): The foreign key referencing the associated user.
        user (relationship): The relationship with the associated user.
        vin (str): The Vehicle Identification Number (VIN) of the car.
        name (str): The name or nickname of the car.
        make (str): The make or manufacturer of the car.
        model (str): The model of the car.
        year (int): The manufacturing year of the car.

    Relationships:
        - 'user': Represents the associated user with a back-ref to 'cars'.
    '''
    __tablename__ = 'cars'
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='cars')
    vin = Column(String(128))
    name = Column(String(128))
    make = Column(String(128))
    model = Column(String(128))
    year = Column(Integer)

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Car class.
        If the VIN is provided, it fetches details using the NHTSA API.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)
        if self.vin:
            url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{}?\
format=json'.format(self.vin)
            response = requests.get(url).json().get('Results')[0]
            if response.get('Make'):
                self.make = response.get('Make')
            if response.get('Model'):
                self.model = response.get('Model')
            if response.get('ModelYear'):
                try:
                    self.year = int(response.get('ModelYear'))
                except ValueError:
                    pass

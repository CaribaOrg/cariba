#!/usr/bin/python3
''' This is a module for Address '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship


class Address(BaseModel, Base):
    '''
    Address class represents a user's address.

    Attributes:
        user_id (str): The foreign key referencing the associated user.
        user (relationship): The relationship with the associated user.
        street (str): The street address.
        city (str): The city of the address.
        state_province (str): The state or province of the address.
        zip_code (int): The ZIP code of the address.

    Relationships:
        - 'user': Represents the associated user with a back-ref to 'address'.
    '''
    __tablename__ = 'addresses'
    user_id = Column(String(128), ForeignKey('users.id'))
    user = relationship('User', back_populates='address')
    street = Column(String(128), nullable=False)
    city = Column(String(128), nullable=False)
    country = Column(String(128), nullable=False)
    zip_code = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Address class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

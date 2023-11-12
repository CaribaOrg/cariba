#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    __tablename__ = 'users'
    username = Column(String(128), nullable=False, unique=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    address = relationship('Address', uselist=False, back_populates='user', cascade='all, delete-orphan')
#    cars = relationship('Car', back_populates='users', cascade='all, delete-orphan')
#    cart_id = Column(String(60), ForeignKey('carts.id'))
    role = Column(String(10), default='user')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

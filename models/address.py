#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

class Address(BaseModel, Base):
    __tablename__ = 'addresses'
    user_id = Column(String(128), ForeignKey('users.id'))
    user = relationship('User', back_populates='address')
    street = Column(String(128), nullable=False)
    city = Column(String(128), nullable=False)
    state_province = Column(String(128), nullable=False)
    zip_code = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

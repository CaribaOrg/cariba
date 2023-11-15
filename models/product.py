#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship

class Product(BaseModel, Base):
    __tablename__ = 'products'
    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
    name = Column(String(128))
    price = Column(Float, nullable=False)
    description = Column(String(1024))
    quantity = Column(Integer)
    oem_number = Column(String(128))
    category = relationship('Category', back_populates='products', uselist=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

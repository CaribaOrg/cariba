#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Category(BaseModel, Base):
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False)
    parent_id = Column(String(60), ForeignKey('categories.id'))
    description = Column(String(1024))
    active = Column(Boolean, default=True)
    icon = Column(String(1024))
    children = relationship('Category', back_populates='parent', remote_side='Category.parent_id')
    parent = relationship('Category', back_populates='children', remote_side='Category.id', uselist=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

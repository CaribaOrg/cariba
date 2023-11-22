#!/usr/bin/python3
''' This is a module for Category '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    '''
    Category class represents a product category.

    Attributes:
        name (str): The name of the category.
        parent_id (str): The foreign key referencing the parent category.
        active (bool): A boolean indicating if the category is active.
        icon (str): The icon associated with the category.
        children (relationship): The relationship with child categories.
        parent (relationship): The relationship with the parent category.
        products (relationship): The relationship with associated products.

    Relationships:
        - 'children': Represents child categories with a back-ref to 'parent'.
        - 'parent': Represents the parent category with back-ref to 'children'.
        - 'products': Represents associated products with cascade delete.
    '''
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False)
    parent_id = Column(String(60), ForeignKey('categories.id'))
    active = Column(Boolean, default=True)
    icon = Column(String(1024))
    children = relationship('Category',
                            back_populates='parent',
                            remote_side='Category.parent_id')
    parent = relationship('Category',
                          back_populates='children',
                          remote_side='Category.id',
                          uselist=False)
    products = relationship('Product',
                            back_populates='category',
                            cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Category class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

#!/usr/bin/python3
''' This is a module for User and Authentication'''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean, DateTime, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from hashlib import md5
from flask_security import UserMixin, RoleMixin, AsaList


class RolesUsers(Base):
    '''
    Docs
    '''
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    '''
    Docs
    '''
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(BaseModel, Base, UserMixin):
    '''
    User class represents a registered user.

    Attributes:
        username (str): The username of the user (unique).
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        password (str): The hashed password of the user.
        email (str): The email address of the user (unique).
        address (relationship): The relationship with the associated address.
        cart (relationship): The relationship with associated shopping cart.
        cars (relationship): The relationship with associated cars.
        orders (relationship): The relationship with associated orders.
        role (str): The role of the user (default='user').

    Relationships:
        - 'address': Represents the associated address.
        - 'cart': Represents the associated shopping cart.
        - 'cars': Represents associated cars with cascade delete.
        - 'orders': Represents associated orders with cascade delete.

    '''
    __tablename__ = 'users'
    username = Column(String(255), unique=True, nullable=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    address = relationship('Address',
                           uselist=False,
                           back_populates='user',
                           cascade='all, delete-orphan')
    cart = relationship('Cart',
                        uselist=False,
                        back_populates='user')
    cars = relationship('Car',
                        back_populates='user',
                        cascade='all, delete-orphan')
    orders = relationship('Order',
                          back_populates='user',
                          cascade='all, delete-orphan')
    role = Column(String(10), default='user')

    def __init__(self, **kwargs):
        from models.cart import Cart
        '''
        Initialize a new instance of the User class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)
        cart_dict = {'user_id': self.id}
        crt = Cart(**cart_dict)
        crt.save()

    def check_password(self, password):
        password = md5(password.encode()).hexdigest()
        return password == self.password

    def get_id(self):
        return self.id

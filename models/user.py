#!/usr/bin/python3
''' This is a module for User and Authentication'''
import json
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean, DateTime, Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from hashlib import md5
from flask_security import UserMixin, RoleMixin, AsaList
from models.notification import Message, Notification
from datetime import datetime


class RolesUsers(Base):
    '''
    Docs
    '''
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', String(60), ForeignKey('users.id'))
    role_id = Column('role_id', String(60), ForeignKey('roles.id'))


class Role(BaseModel, Base, RoleMixin):
    '''
    Docs
    '''
    __tablename__ = 'roles'
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
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True)
    phone = Column(Integer)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    last_message_read_time = Column(DateTime())
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
    wishlist_items = relationship('WishlistItem',
                                  uselist=True,
                                  back_populates='user')
    messages_sent = relationship('Message',
                                 foreign_keys='Message.sender_id', back_populates='author')
    messages_received = relationship('Message',
                                     foreign_keys='Message.recipient_id', back_populates='recipient')
    notifications = relationship('Notification', back_populates='user')

    def unread_message_count(self):
        from models import strg
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        number_of_unread = strg.session.query(Message).filter_by(
            recipient_id=self.id).filter(Message.updated_at > last_read_time).count()
        return number_of_unread

    def add_notification(self, name, data):
        from models import strg
        strg.session.query(Notification).filter_by(name=name).delete()
        strg.save()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        strg.save()
        return n

    def __init__(self, **kwargs):
        from models.cart import Cart
        from models.address import Address
        '''
        Initialize a new instance of the User class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)
        cart_dict = {'user_id': self.id}
        crt = Cart(**cart_dict)
        crt.save()
        address_dict = {'user_id': self.id}
        address = Address(**address_dict)
        address.save()

    def check_password(self, password):
        password = md5(password.encode()).hexdigest()
        return password == self.password

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_admin(self):
        """heck if the user is an admin"""
        return 'admin' in self.roles

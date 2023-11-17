#!/usr/bin/python3
''' This is a module for Storage '''

from models.base_model import BaseModel, Base
from models.user import User
from models.address import Address
from models.car import Car
from models.cart import Cart
from models.cart_item import CartItem
from models.category import Category
from models.product import Product
from models.order import Order
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv


class Storage:
    '''
    Storage class manages the database engine and sessions.

    Attributes:
        __engine: The database engine instance.
        __session: The database session instance.
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
        Initialize a new instance of the Storage class.
        Initializes the database engine with MySQL configuration.
        '''
        CARIBA_MYSQL_USER = getenv('CARIBA_MYSQL_USER')
        CARIBA_MYSQL_PWD = getenv('CARIBA_MYSQL_PWD')
        CARIBA_MYSQL_HOST = getenv('CARIBA_MYSQL_HOST')
        CARIBA_MYSQL_DB = getenv('CARIBA_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(CARIBA_MYSQL_USER,
                                              CARIBA_MYSQL_PWD,
                                              CARIBA_MYSQL_HOST,
                                              CARIBA_MYSQL_DB))

    def new(self, obj):
        '''
        Add a new object to the current database session.

        Args:
            obj: The object to be added to the session.
        '''
        self.__session.add(obj)

    def save(self):
        ''' Commit the current database session. '''
        self.__session.commit()

    def reload(self):
        ''' Reload the database engine and create a new session. '''
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def delete(self, obj=None):
        '''
        Delete an object from the current database session.

        Args:
            obj: The object to be deleted from the session (default=None).
        '''
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        ''' Close the current database session. '''
        self.__session.remove()

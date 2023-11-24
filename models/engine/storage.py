#!/usr/bin/python3
''' This is a module for Storage '''

from models.base_model import BaseModel, Base
from models.user import User, Role, RolesUsers
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
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(CARIBA_MYSQL_USER,
                                              CARIBA_MYSQL_PWD,
                                              CARIBA_MYSQL_HOST,
                                              CARIBA_MYSQL_DB))
        
    def all(self, cls=None):
        '''
        Retrieve all objects of the specified class or a list of classes.

        Args:
            cls (type or list[type], optional): The class to query.
                If not provided, the method retrieves all objects
        '''
        if cls is None:
            cls = [User, Address, Car, Cart, CartItem, Category, Product, Order]
            query = []
            for c in cls:
                query.extend(self.__session.query(c).all())
        else:
            query = self.__session.query(cls).all()
        objs = []
        for obj in query:
            objs.append(obj)
        return objs

    def search(self, **kwargs):
        '''
        Search for objects based on specified attribute-value pairs.

        Args:
            **kwargs: Keyword arguments representing attribute-value pairs.
                - cls (type, optional): The class to search within.
                - case_sensitive (bool, optional): Whether the search should be
                            case-sensitive (default is True).
                - exact (bool, optional): Whether the search should match values
                            exactly (default is True).
                - Other keyword arguments are treated as attribute-value pairs
                            for filtering.

        Returns:
            list: A list containing objects that match the specified criteria.
        '''
        cls = kwargs.get('cls', None)
        case_sensitive = kwargs.get('case_sensitive', True)
        exact = kwargs.get('exact', True)
        kwargs.pop('cls', None)
        kwargs.pop('case_sensitive', None)
        kwargs.pop('exact', None)
        all_objs = self.all(cls)
        result = []
        for obj in all_objs:
            matched = True
            for key, value in kwargs.items():
                current_exact = exact
                current_case_sensitive = case_sensitive
                obj_value = getattr(obj, key, None)
                if not isinstance(obj_value, str) or not isinstance(value, str):
                    current_exact = True
                    current_case_sensitive = True
                if not current_case_sensitive:
                    value = value.lower()
                    obj_value = obj_value.lower()
                if current_exact:
                    if value != obj_value:
                        matched = False
                        break
                else:
                    if value not in obj_value:
                        matched = False
                        break
            if matched:
                result.append(obj)
        if len(result) == 1:
            return result[0]
        return result

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
        self.__session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self.__engine))
        Base.query = self.__session.query_property()
        Base.metadata.create_all(bind=self.__engine)

    def delete(self, obj=None):
        '''
        Delete an object from the current database session.

        Args:
            obj: The object to be deleted from the session (default=None).
        '''
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def expire(self, obj):
        if obj is not None:
            self.__session.expire(obj)

    def close(self):
        ''' Close the current database session. '''
        self.__session.remove()
    
    @property
    def session(self):
        '''
        Docs
        '''
        return self.__session

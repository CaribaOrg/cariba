#!/usr/bin/python3

from models.base_model import BaseModel, Base
from models.user import User
from models.address import Address
#from models.car import Car
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class Storage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format('root', 'root', '172.17.0.3', 'db'))

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        self.__session.remove()

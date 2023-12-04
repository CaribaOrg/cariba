#!/usr/bin/python3
''' This is a module for Order '''

import json
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Message(BaseModel, Base):
    '''
    Order class represents a user's order.

    Attributes:
        sender_id (str): The foreign key referencing the associated user.
        recipient_id (str): The foreign key referencing the associated user.
        body (str): The Message body
        author (relationship): The relationship with the associated user.
        recipient (relationship): The relationship with the associated user.

    Relationships:
        - 'author': Represents the associated user with a back-ref to 'orders'.
        - 'recipient': Represents the associated cart.
    '''
    __tablename__ = 'messages'
    body = Column(String(2555), nullable=False)
    sender_id = Column(String(128), ForeignKey('users.id'))
    recipient_id = Column(String(128), ForeignKey('users.id'))
    
    author = relationship('User',
        foreign_keys='Message.sender_id',
        back_populates='messages_sent')
    recipient = relationship('User',
        foreign_keys='Message.recipient_id',
        back_populates='messages_received')
    
    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Order class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

class Notification(BaseModel, Base):
    '''
    Order class represents a user's order.

    Attributes:
        user_id (str): The foreign key referencing the associated user.
        user (relationship): The relationship with the associated user.
        name (str): The status of the order.
        payload_json (str): The foreign key referencing the associated cart.

    Relationships:
        - 'user': Represents the associated user with a back-ref to 'orders'.
    '''
    __tablename__ = 'notifications'
    user_id = Column(String(128), ForeignKey('users.id'))
    user = relationship('User', back_populates='notifications')
    name = Column(String(128))
    payload_json = Column(Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Order class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)

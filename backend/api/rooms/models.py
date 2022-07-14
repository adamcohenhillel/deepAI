"""Deeper 2022, All Rights Reserved
"""
from datetime import datetime as dt
from sqlalchemy import Column, Integer, ForeignKey, Table, String, DateTime
from sqlalchemy.orm import relationship, backref

from db.models.base import Base


users_rooms = Table('users_rooms',
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('room_id', Integer, ForeignKey('rooms.id'), primary_key=True)
)

class Room(Base):
    """
    """
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    users = relationship('Users', secondary=users_rooms, lazy='subquery', backref=backref('rooms', lazy=True))
    messages = relationship('RoomMessages', backref='room', lazy=True)

class RoomMessages(Base):
    """
    """
    __tablename__ = 'room_messages'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    message = Column(String, nullable=False)
    sent = Column(DateTime, default=dt.utcnow)

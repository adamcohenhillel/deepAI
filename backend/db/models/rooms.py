"""Deeper 2022, All Rights Reserved
"""
from datetime import datetime as dt
from sqlalchemy import Column, Integer, ForeignKey, Table, String, DateTime
from sqlalchemy.orm import relationship, backref

from db.models.base import Base


users_rooms = Table(
    'users_rooms',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('room_id', Integer, ForeignKey('rooms.id'), primary_key=True)
)


class Room(Base):
    """
    """
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    users = relationship('User', secondary=users_rooms, lazy='selectin', backref=backref('rooms', lazy='selectin'))
    messages = relationship('RoomMessage', backref='room', lazy='selectin')

    @property
    def channel(self) -> str:
        return f'room:{self.id}'


class RoomMessage(Base):
    """
    """
    __tablename__ = 'room_messages'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(String, nullable=False)
    sent = Column(DateTime, default=dt.utcnow)
    user = relationship('User', lazy='selectin')

    @property
    def message(self) -> str:
        return f'{self.user.username}:{self.text}'

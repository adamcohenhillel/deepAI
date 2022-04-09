"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from sqlalchemy import Column, Integer

from core.ext import Base


class Room(Base):
    """
    """
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    
    # users = Column(String, nullable=False, unique=True)
    
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

class RoomChat(Base):
    """
    """
    pass
    
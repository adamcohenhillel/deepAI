"""Deeper 2022, All Rights Reserved
"""
from sqlalchemy import Column, Integer, String

from core.ext import Base


class User(Base):
    """
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str  = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)

    # TODO: Add email? some identiney verification?
    # TODO: Add back relationship to matches

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
    
    def __repr__(self) -> str:
        return f'<User {self.username} ({self.id})'

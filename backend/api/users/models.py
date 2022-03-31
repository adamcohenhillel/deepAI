"""
"""
from sqlalchemy import Column, Integer, ForeignKey, String

from core.ext import Base


class User(Base):
    """
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # TODO: Add email? some identiney verification?
    # TODO: Add back relationship to matches

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
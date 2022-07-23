"""Deeper 2022, All Rights Reserved
"""
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext

from db.models.base import Base


_pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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
        self.password = self.hash_password(password)
    
    def __repr__(self) -> str:
        return f'<User {self.username} ({self.id})'

    def hash_password(self, password: str) -> str:
        """
        """
        return _pwd_context.hash(password)
    
    def verify_password(self, plain_password: str) -> bool:
        """
        """
        return _pwd_context.verify(plain_password, self.password)

"""
"""
from sqlalchemy import Column, Integer, ForeignKey, String

from core.ext import Base


class MatchRequest(Base):
    __tablename__ = 'matchrequests'
    
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)
    raw_request = Column(String, nullable=False)
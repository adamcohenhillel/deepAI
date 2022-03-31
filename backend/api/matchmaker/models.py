"""
"""
from email.policy import default
from sqlalchemy import Column, Integer, ForeignKey, String

from core.ext import Base


MATCHREQUEST_STATES = {'open', 'fresh', 'close'}


class MatchRequest(Base):
    """MatchRequest is the equivillant of "tweet" in twitter - 
    you just say whatevcer is on your mind and the platform find 
    a match for you based on the matchrequest characteristic
    """
    __tablename__ = 'matchrequests'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    raw_request = Column(String, nullable=False)
    state = Column(String, nullable=False, default='fresh')

    def __init__(self, user_id, raw_request) -> None:
        self.user_id = user_id
        self.raw_request = raw_request

    def set_state(self, state: str) -> None:
        """
        """
        if state not in MATCHREQUEST_STATES:
            raise Exception # TODO: Something else is required here
        self.state = state

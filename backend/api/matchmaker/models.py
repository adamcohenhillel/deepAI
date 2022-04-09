"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship, backref


from core.ext import Base


MATCHREQUEST_STATES = {'open', 'fresh', 'close'}

tags_requests_association = Table(
    'tags_requests_association',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('matchrequest_id', Integer, ForeignKey('matchrequests.id'), primary_key=True),
)


class Tag(Base):
    """
    """
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # TODO: Add vector

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
    tags = relationship(  # TODO: Optomize this relationship, will be a bottleneck kater on!
        'Tag',
        secondary=tags_requests_association,
        lazy='joined',
        backref=backref('MatchRequest')
    )

    def __init__(self, user_id, raw_request) -> None:
        self.user_id = user_id
        self.raw_request = raw_request

    def set_state(self, state: str) -> None:
        """
        """
        if state not in MATCHREQUEST_STATES:
            raise Exception # TODO: Something else is required here
        self.state = state

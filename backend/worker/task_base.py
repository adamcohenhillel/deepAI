"""Adam Cohen Hillel 2022, All Rights Reserved
"""
import logging

from celery.contrib.abortable import AbortableTask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, Session, sessionmaker
from config import APIProdConfig


class TaskBase(AbortableTask):
    """Base for all celery tasks in the app,
    providing access to the database
    """
    _session = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @property
    def session(self) -> Session:
        """
        """
        if not self._session:
            engine = create_engine(APIProdConfig.SQLALCHEMY_DATABASE_URI)  #TODO: Have different way for config
            session = scoped_session(sessionmaker(bind=engine))()
            self._session = session
        return self._session
    
    def write_to_db(self, data) -> None:
        """
        """
        pass


        

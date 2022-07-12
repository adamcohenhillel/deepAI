"""
"""
from contextlib import contextmanager

from neo4j import GraphDatabase, Session


class Neo4jDBConnector:
    """
    """
    def __init__(self, uri: str, user: str, password: str) -> None:
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self._driver.close()

    @contextmanager
    def use_session(self) -> Session:
        with self._driver.session() as session:
            yield session

"""
"""
from contextlib import contextmanager

from neo4j import GraphDatabase


class Neo4jDBConnector:
    """
    """

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    @contextmanager
    def use_session(self):
        with self._driver.session() as session:
            yield session

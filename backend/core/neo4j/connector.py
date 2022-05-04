"""
"""
from contextlib import contextmanager
from typing import List, Type

from neo4j import GraphDatabase
from core.neo4j.entities import DeepRequestNode
from core.neo4j.entities import _Neo4jNode


class Neo4jDBConnector:
    """
    """

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._nodes: List[Type[_Neo4jNode]] = _Neo4jNode.__subclasses__()

    def close(self):
        self._driver.close()

    @contextmanager
    def use_session(self):
        with self._driver.session() as session:
            yield session

    def testme(self):
        with self.use_session() as session:
            session.write_transaction(DeepRequestNode.create, "WHATTT")

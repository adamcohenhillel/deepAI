"""ORM-like approach to neo4j nodes
"""
from abc import ABC, abstractmethod
from typing import Any


class _Neo4jNode(ABC):
    """
    """

    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError

    # @staticmethod
    # @abstractmethod
    # def dependency(self) -> None:
    #     raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError


class DeepRequestNode(_Neo4jNode):
    """
    """
    label = 'DeepRequest'

    @staticmethod
    def create(tx, raw_request) -> int:
        query = "CREATE (node:DeepRequest { request: $raw_request }) RETURN ID(node) AS node_id"
        result = tx.run(query, raw_request=raw_request)
        record = result.single()
        return record["node_id"]


# class DescriberNode(_Neo4jNode):
#     """
#     """
#     label = "DescriberNode"

#     def dependency(self, tx) -> None:
#         query = "CREATE CONSTRAINT ON (node:$label) ASSERT node.describer IS UNIQUE"
#         tx.run(query, label=self.label)
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
        query = "CREATE (n:DeepRequest { request: $raw_request }) RETURN ID(n) AS node_id"
        result = tx.run(query, raw_request=raw_request)
        record = result.single()
        return record["node_id"]


class AdjectiveNode(_Neo4jNode):
    """
    """
    label = "AdjectiveNode"
    
    @staticmethod
    def create(tx, value) -> int:
        query = "MERGE (n:AdjectiveNode { adjective: $value }) RETURN ID(n) AS node_id"
        result = tx.run(query, value=value)
        record = result.single()
        return record["node_id"]


class RequestAdjectiveRealtionship(_Neo4jNode):

    @staticmethod
    def create(tx, request_node_id, adjective_node_id) -> int:
        query = "MATCH (a), (b) WHERE ID(a) = $request_node_id AND ID(b) = $adjective_node_id MERGE (a)-[r:IS]->(b) RETURN ID(r) as relationship_id"
        result = tx.run(query, request_node_id=request_node_id, adjective_node_id=adjective_node_id)
        record = result.single()
        return record["relationship_id"]
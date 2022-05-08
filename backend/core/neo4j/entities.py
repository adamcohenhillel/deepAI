"""ORM-like approach to neo4j nodes
"""
from abc import ABC, abstractmethod


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
    
    @staticmethod
    def matched_nodes(tx, deep_id, number_of_related):
        query = """
        MATCH (d1:DeepRequest)-->(a:AdjectiveNode)<--(d2:DeepRequest)
        WHERE ID(d1) = $deep_id 
        WITH d1, d2, collect(a) as related_adjectives
        WHERE size(related_adjectives) > $number_of_related
        RETURN d1, d2, related_adjectives
        """
        result = tx.run(query, deep_id=deep_id, number_of_related=number_of_related)
        record = result.single()
        return record["node_id"]


class AdjectiveNode(_Neo4jNode):
    """
    """
    label = "AdjectiveNode"
    
    @staticmethod
    def create(tx, adjective, key) -> int:
        query = "MERGE (n:AdjectiveNode { adjective: $adjective, key: $key }) RETURN ID(n) AS node_id"
        result = tx.run(query, adjective=adjective, key=key)
        record = result.single()
        return record["node_id"]


class RequestAdjectiveRealtionship(_Neo4jNode):

    @staticmethod
    def create(tx, request_node_id, adjective_node_id) -> int:
        query = "MATCH (a), (b) WHERE ID(a) = $request_node_id AND ID(b) = $adjective_node_id MERGE (a)-[r:IS]->(b) RETURN ID(r) as relationship_id"
        result = tx.run(query, request_node_id=request_node_id, adjective_node_id=adjective_node_id)
        record = result.single()
        return record["relationship_id"]
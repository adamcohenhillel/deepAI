"""ORM-like approach to neo4j nodes
"""
from abc import ABC, abstractmethod


class _Neo4jObject(ABC):

    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, tx, **kwargs) -> int:
        raise NotImplementedError


class _Node(_Neo4jObject):
    """
    """

    @classmethod
    def _raw_query(cls, tx, action: str, **kwargs) -> int:
        _keys_str = ', '.join([f'{k}: ${k}' for k in kwargs])  # Creates a string as follow: key1: $key1, key2: $key2,  
        query = f'{action} (n:{cls.label} {{{_keys_str}}}) RETURN ID(n) AS node_id'
        result = tx.run(query, **kwargs)
        record = result.single()
        return record['node_id']

    @classmethod
    def create(cls, tx, **kwargs) -> int:
        return cls._raw_query(tx, 'CREATE', **kwargs)
    
    @classmethod
    def get_or_create(cls, tx, **kwargs) -> int:
        return cls._raw_query(tx, 'MERGE', **kwargs)


class DeepRequestNode(_Node):
    label = 'DeepRequest'
    
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
        return record['node_id']


class UserNode(_Node):
    label = 'UserNode'


class AdjectiveNode(_Node):
    label = 'AdjectiveNode'


class _Realtionship(_Neo4jObject):

    @classmethod
    def create(cls, tx, match_a, match_b) -> int:
                ID(a) = $request_node_id AND ID(b) = $adjective_node_id
        query = f"MATCH (a), (b) WHERE {match_a} AND {match_b} MERGE (a)-[r:{cls.label}]->(b) RETURN ID(r) as relationship_id"
        result = tx.run(query, request_node_id=request_node_id, adjective_node_id=adjective_node_id)
        record = result.single()
        return record['relationship_id']

class RequestAdjectiveRealtionship(_Realtionship):
    """
    """
    label = 'IS'

    @classmethod
    def create(cls, tx, request_node_id, adjective_node_id) -> int:
        query = "MATCH (a), (b) WHERE ID(a) = $request_node_id AND ID(b) = $adjective_node_id MERGE (a)-[r:IS]->(b) RETURN ID(r) as relationship_id"
        result = tx.run(query, request_node_id=request_node_id, adjective_node_id=adjective_node_id)
        record = result.single()
        return record['relationship_id']


class UserDeepRequestRealtionship(_Node):
    """
    """

    @classmethod
    def create(cls, tx, user_id, deeprequest_id) -> int:
        popup = 'created'
        query = f"MATCH (a), (b) WHERE a.user_id = $user_id AND ID(b) = $deeprequest_id MERGE (a)-[r:{popup}]->(b) RETURN ID(r) as relationship_id"
        result = tx.run(query, user_id=user_id, deeprequest_id=deeprequest_id)
        record = result.single()
        return record['relationship_id']

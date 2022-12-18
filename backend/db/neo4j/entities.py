"""ORM-like approach to neo4j nodes
"""
import json
from abc import ABC, abstractmethod
from typing import Literal


class _Neo4jObject(ABC):

    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError('This method must be implemented')

    @classmethod
    @abstractmethod
    def create(cls, tx, **kwargs) -> int:
        raise NotImplementedError('This method must be implemented')


class _Node(_Neo4jObject):
    """
    """

    @classmethod
    def _raw_query(
        cls,
        tx,
        creation_action: Literal['MERGE', 'CREATE'],
        **kwargs
    ) -> int:
        obj = ', '.join([f'{k}: {json.dumps(v)}' for k, v in kwargs.items()])  # Creates a string as follow: key1: $key1, key2: $key2,  
        query = f'{creation_action} (n:{cls.label} {{{obj}}}) RETURN ID(n) AS node_id'
        result = tx.run(query)
        record = result.single()
        return record['node_id']

    @classmethod
    def create(cls, tx, **kwargs) -> int:
        return cls._raw_query(tx, 'CREATE', **kwargs)

    @classmethod
    def get_or_create(cls, tx, **kwargs) -> int:
        return cls._raw_query(tx, 'MERGE', **kwargs)


class _Realtionship(_Neo4jObject):
    """
    """

    @classmethod
    def _raw_query(
        cls,
        tx,
        creation_action: Literal['CREATE', 'MERGE'],
        condition: str
    ) -> int:
        """Match two nodes and creates a relationship between them

        :param tx: Neo4j transaction object
        :param creation_action: How to create the relationship
        :param condition: How to find the two nodes: a, b
        """
        query = f'MATCH (a), (b) WHERE {condition} {creation_action} (a)-[r:{cls.label}]->(b) RETURN ID(r) as relationship_id'
        result = tx.run(query)
        record = result.single()
        return record['relationship_id']


class DeepRequestNode(_Node):
    label = 'DeepRequest'


class UserNode(_Node):
    label = 'UserNode'


class AdjectiveNode(_Node):
    label = 'AdjectiveNode'


class RequestAdjectiveRealtionship(_Realtionship):
    label = 'IS'

    @classmethod
    def get_or_create(cls, tx, node_a_id, node_b_id):
        cls._raw_query(tx, 'MERGE', f'ID(a) = {node_a_id} AND ID(b) = {node_b_id}')


class UserDeepRequestRealtionship(_Realtionship):
    label = 'REQUESTED'

    @classmethod
    def get_or_create(cls, tx, node_a_id, node_b_id):
        cls._raw_query(tx, 'MERGE', f'a.user_id = {node_a_id} AND ID(b) = {node_b_id}')


    # @staticmethod
    # def matched_nodes(tx, deep_id, number_of_related):
    #     query = """
    #     MATCH (d1:DeepRequest)-->(a:AdjectiveNode)<--(d2:DeepRequest)
    #     WHERE ID(d1) = $deep_id 
    #     WITH d1, d2, collect(a) as related_adjectives
    #     WHERE size(related_adjectives) > $number_of_related
    #     RETURN d1, d2, related_adjectives
    #     """
    #     result = tx.run(query, deep_id=deep_id, number_of_related=number_of_related)
    #     record = result.single()
    #     return record['node_id']
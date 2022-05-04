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



# def add_friend(tx, name, friend_name):
#     tx.run("MERGE (a:Person {name: $name}) "
#            "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
#            name=name, friend_name=friend_name)

# def print_friends(tx, name):
#     for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
#                          "RETURN friend.name ORDER BY friend.name", name=name):
#         print(record["friend.name"])

# with driver.session() as session:
#     session.write_transaction(add_friend, "Arthur", "Guinevere")
#     session.write_transaction(add_friend, "Arthur", "Lancelot")
#     session.write_transaction(add_friend, "Arthur", "Merlin")
#     session.read_transaction(print_friends, "Arthur")



class DeepRequestNode(_Neo4jNode):
    """
    """
    label = 'DeepRequest'

    def create(tx, raw_request) -> Any:
        query =  "CREATE (node:DeepRequest { request: $raw_request }) RETURN node"
        tx.run(query, raw_request=raw_request)


# class DescriberNode(_Neo4jNode):
#     """
#     """
#     label = "DescriberNode"

#     def dependency(self, tx) -> None:
#         query = "CREATE CONSTRAINT ON (node:$label) ASSERT node.describer IS UNIQUE"
#         tx.run(query, label=self.label)
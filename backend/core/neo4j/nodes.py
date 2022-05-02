"""ORM-like approach to neo4j nodes
"""


class _Neo4jNode:
    """
    """
    def create(self, *args, **kwargs):
        raise NotImplementedError


class UserNode(_Neo4jNode):
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)


class MatchRequestNode(_Neo4jNode):
    pass


class DescriberNode(_Neo4jNode):
    pass
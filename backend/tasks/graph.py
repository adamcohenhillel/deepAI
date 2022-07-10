"""Deeper 2022, All Rights Reserved
"""
import logging
from typing import Dict
from db.neo4j.entities import AdjectiveNode, RequestAdjectiveRealtionship


async def add_describers_nodes(neo4j_session, data: Dict, node_id) -> None:
    """
    """
    for label, values in data.items():
        for value in values:
            new_node_id = neo4j_session.write_transaction(AdjectiveNode.create, adjective=value, key=label)
            realtionship_id = neo4j_session.write_transaction(RequestAdjectiveRealtionship.create, node_id, new_node_id)

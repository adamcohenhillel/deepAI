"""Deeper 2022, All Rights Reserved
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from db.neo4j.entities import DeepRequestNode
from db.dependencies import get_neo4j_connector
from tasks.pipelines import analyze_deep_request


deeprequests_router = APIRouter()


class DeepRequestSchema(BaseModel):
    deep_request: str


@deeprequests_router.post('/')
async def post(
    body: DeepRequestSchema,
    background_tasks: BackgroundTasks,
    neo4j_connector = Depends(get_neo4j_connector),
):
    """Create a new deep request

    :param body: request Json parameters
    :param background_tasks: Interface to FastAPI background tasks
    :param neo4j_connector: Connector details to
    """
    with neo4j_connector.use_session() as session:
        new_node_id = session.write_transaction(
            DeepRequestNode.create,
            body.deep_request
        )
    background_tasks.add_task(
        analyze_deep_request,
        neo4j_connector,
        body.deep_request,
        new_node_id
    )
    return {'node': new_node_id}

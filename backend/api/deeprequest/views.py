"""Deeper 2022, All Rights Reserved
"""
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sanic import Blueprint, Request
from sanic.response import json, HTTPResponse
from sanic_jwt import protected

from api.deeprequest.schemas import DeepRequestSchema
from core.neo4j.entities import DeepRequestNode
from tasks.pipelines import analyze_deep_request


class DeepRequestResource(HTTPMethodView):
    """Resource to handle deep request 
    """

    async def get(self, request: Request) -> HTTPResponse:
        """Get all deep requests of a user (self)
        """
        pass
    
    @protected()
    @validate(json=DeepRequestSchema)
    async def post(self, request: Request, body: DeepRequestSchema) -> HTTPResponse:
        """Create a new deep request
        """
        with request.ctx.neo4j.use_session() as session:
            new_node_id = session.write_transaction(
                DeepRequestNode.create,
                body.deep_request
            )

        request.app.add_task(analyze_deep_request(request.ctx.neo4j, body.deep_request, new_node_id))
        return json(body={'node': new_node_id}, status=201)


deeprequest_bp = Blueprint('deeprequest_bp', url_prefix='/deeprequest')
deeprequest_bp.add_route(DeepRequestResource.as_view(), '/')

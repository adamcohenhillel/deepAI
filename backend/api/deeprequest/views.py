"""Deeper 2022, All Rights Reserved
"""
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sanic import Blueprint
from sanic.response import json

from api.deeprequest.schemas import DeepRequestSchema
from core.neo4j.entities import DeepRequestNode
from tasks.pipelines import analyze_deep_request


class DeepRequestResource(HTTPMethodView):
    """Resource to handle deep request 
    """

    async def get(self, request):
        """Get all deep requests of a user (self)
        """
        pass
    
    @validate(json=DeepRequestSchema)
    async def post(self, request, post_data):
        """Create a new deep request
        """
        with request.ctx.neo4j.use_session() as session:
            new_node_id = session.write_transaction(
                DeepRequestNode.create,
                post_data['deep_request']
            )

        request.app.add_task(analyze_deep_request(request.ctx.neo4j, post_data['deep_request'], new_node_id))
        return json(body={'node': new_node_id}, status=201)


deeprequest_bp = Blueprint('deeprequest_bp', url_prefix='/deeprequest')
deeprequest_bp.add_route(DeepRequestResource.as_view(), '/')

"""Deeper 2022, All Rights Reserved
"""
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage
# from worker.pipelines import analyze_deep_request
from sanic import Blueprint
from sanic.response import json

from core.neo4j.entities import DeepRequestNode

class DeepRequestResource(HTTPMethodView):
    """
    """

    async def get(self, request):
        pass

    async def post(self, request):
        """
        """
        post_data = request.json or {}

        if 'deep_request' not in post_data:
            raise InvalidUsage('deep_request must be provided')

        with request.ctx.neo4j.use_session() as session:
            new_node_id = session.write_transaction(
                DeepRequestNode.create, post_data['deep_request'])

        # analyze_deep_request(post_data['deep_request'], new_node_id, celery_app=current_app.worker)()
        return json(node=new_node_id), 201


deeprequest_bp = Blueprint('deeprequest_bp', url_prefix='/deeprequest')
deeprequest_bp.add_route(DeepRequestResource.as_view(), '/')

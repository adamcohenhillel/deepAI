"""Adam Cohen Hillel 2022, All Rights Reserved
"""
import json
import logging

from flask import Blueprint, jsonify, request, current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.exceptions import BadRequest
from core.neo4j.entities import DeepRequestNode

from core.ext import db


deeprequest_bp = Blueprint('deeprequest_bp', __name__)

    
class DeepRequestResource(MethodView):
    """
    """

    def get(self):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        pass
    
    # @jwt_required
    def post(self):
        """
        """
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        post_data = request.get_json() or {}

        if 'raw_request' not in post_data:
            raise BadRequest('raw_request must be provided')

        with current_app.neo4j.use_session() as session:
            session.write_transaction(DeepRequestNode.create, "WHATTT")
        
        # current_app.worker.send_task('text_analyzer', args=(new_request.id,))
        return jsonify(msg='Created'), 201
    
    # def put(self):
    #     pass
    
    # def delete(self):
    #     pass

        
deeprequest_bp.add_url_rule('/', view_func=DeepRequestResource.as_view('deeprequest_resource'))

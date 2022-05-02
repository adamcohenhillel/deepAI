"""Adam Cohen Hillel 2022, All Rights Reserved
"""
import json
import logging

from flask import Blueprint, jsonify, request, current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from api.matchmaker.models import MatchRequest
from api.matchmaker.schemas import MatchRequestSchema
from core.ext import db


matchmaker_bp = Blueprint('matchmaker_bp', __name__)


class MatchmakerResource(MethodView):
    """
    """

    def get(self):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user_data = MatchRequest.query.filter_by(user_id=user_id).all()
        return jsonify(MatchRequestSchema(many=True).dump(user_data)), 200
    
    # @jwt_required
    def post(self):
        """
        """
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        post_data = request.get_json() or {}
        validated_data = MatchRequestSchema().load(post_data)

        new_request = MatchRequest(user_id=user_id, **validated_data)
        db.session.add(new_request)
        db.session.commit()
        current_app.worker.send_task('text_analyzer', args=(new_request.id,))
        return jsonify(msg='Created'), 201
    
    # def put(self):
    #     pass
    
    # def delete(self):
    #     pass

        
matchmaker_bp.add_url_rule('/', view_func=MatchmakerResource.as_view('matchmaker_resource'))

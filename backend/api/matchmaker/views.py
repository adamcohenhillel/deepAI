"""Adam Cohen Hillel 2022, All Rights Reserved
"""
import logging

from flask import Blueprint, request
from flask.views import MethodView

from api.matchmaker.models import MatchRequest

matchmaker_bp = Blueprint('matchmaker_bp', __name__)


class MatchmakerResource(MethodView):
    """
    """

    def get(self):
        user_data = MatchRequest.query.filter_by().all()
    
    # TODO: Add some kind of authentication
    def post(self):
        """
        """
        data = request.get_json()
        # TODO: Add data validation (marshmallow?)
    
    def put(self):
        pass
    
    def delete(self):
        pass
        



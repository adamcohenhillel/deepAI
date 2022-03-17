"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from flask import Blueprint
from flask.views import MethodView

matchmaker_bp = Blueprint('matchmaker_bp')


class MatchMakerResource(MethodView):
    """
    """
    
    def get(self):
        """Get all matching queue
        """
        pass

    def post(self):
        """Request for a new match
        """
        pass


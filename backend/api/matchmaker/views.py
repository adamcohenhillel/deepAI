"""Adam Cohen Hillel 2022, All Rights Reserved
"""

from flask import Blueprint, request
from flask.views import MethodView


matchmaker_bp = Blueprint('matchmaker_bp')


class MatchmakerResource(MethodView):
    """
    """

    def get(self):
        pass
    
    # TODO: Add some kind of authentication
    def post(self):
        """
        """
        data = request.get_json()
        # TODO: Add data validation (marshmallow?)
        



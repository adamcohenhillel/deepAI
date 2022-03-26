
"""
"""
from flask import Blueprint
from flask.views import MethodView

from api.users.models import User


users_bp = Blueprint('users_bp', __name__)


class UsersListResource(MethodView):
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
        



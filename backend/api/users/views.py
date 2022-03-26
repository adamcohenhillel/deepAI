
"""
"""
from flask import Blueprint, jsonify, request
from flask.views import MethodView

from api.users.models import User
from api.users.schemas import UserSchema
from core.ext import db
from api.utils import api_response


users_bp = Blueprint('users_bp', __name__)


class UsersListResource(MethodView):
    """
    """

    def get(self):
        pass
        # user_data = MatchRequest.query.filter_by().all()
    
    # TODO: Add some kind of authentication
    def post(self):
        """
        """
        post_data = request.get_json() or {}
        validated_data = UserSchema().load(post_data)
        new_user = User(**validated_data)
        db.session.add(new_user)
        db.session.commit()

        return api_response('New user was created', 201)
    
    def put(self):
        pass
    
    def delete(self):
        pass


users_bp.add_url_rule('/', view_func=UsersListResource.as_view('users_list_resource'))

"""Deeper 2022, All Rights Reserved
"""

from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json

from api.users.models import User
from api.users.schemas import UserSchema

users_bp = Blueprint('users_bp', __name__)


class UsersListResource(HTTPMethodView):
    """
    """

    async def get(self, request):
        pass

    async def post(self, request):
        """Create a new user
        """
        session = request.ctx.session
        async with session.begin():
            post_data = request.json or {}
            new_user = User(**post_data)
            session.add_all([new_user])
        return json(msg='New user created')


class AccessTokensResource(HTTPMethodView):
    """Generate access tokens for users
    """

    async def post(self):
        # post_data = request.get_json() or {}
        # validated_data = UserSchema().load(post_data)

        # user = User.query.filter_by(
        #     username=validated_data['username']).first()
        # if not user:
        #     raise BadRequest('Username or password are incorrect')

        # access_token = create_access_token(identity=user.id)
        return json(access_token='temp')


users_bp = Blueprint('users_bp', url_prefix='/users')
users_bp.add_route(UsersListResource.as_view(), '/')
users_bp.add_route(AccessTokensResource.as_view(), '/auth')

"""Deeper 2022, All Rights Reserved
"""
from sanic_ext import validate
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json
from api.users.models import User
from api.users.schemas import UserSchema
from core.neo4j.entities import DeepRequestNode
users_bp = Blueprint('users_bp', __name__)


class UsersListResource(HTTPMethodView):
    """
    """

    async def get(self, request):
        return json(body={'message': 'not implemeneted just yet'})

    # @validate(json=UserSchema)
    async def post(self, request):
        """Create a new user
        """
        session = request.ctx.session
        async with session.begin():
            new_user = User(**request.json)
            session.add_all([new_user])
        return json(body={'message':'New user created'})


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

"""Deeper 2022, All Rights Reserved
"""
from typing import Dict
from sanic import Blueprint, Request
from sanic.views import HTTPMethodView
from sanic.response import json, HTTPResponse
from sanic.exceptions import HeaderNotFound
from sanic_ext import validate
from sanic_jwt.exceptions import AuthenticationFailed
from sqlalchemy.future import select

from api.users.models import User
from api.users.schemas import UserSchema


users_bp = Blueprint('users_bp', __name__)


class UsersListResource(HTTPMethodView):
    """
    """

    @validate(json=UserSchema)
    async def post(self, request: Request, body: UserSchema) -> HTTPResponse:
        """Create a new user
        """
        session = request.ctx.session
        async with session.begin():
            new_user = User(username=body.username, password=body.password)
            session.add_all([new_user])
        return json(body={'message': 'Created'}, status=201)


async def authenticate(request: Request) -> Dict:
    """Authentricate user based on username and password
    """
    if not request.json:
        raise HeaderNotFound('Json must be provided') 

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not (username or password):
        raise AuthenticationFailed('Missing username or password')

    async with request.ctx.session.begin():
        query = select(User).where(User.username == username)
        result = await request.ctx.session.execute(query)
        user = result.scalar()
    
    if user is None or password != user.password:
        raise AuthenticationFailed("Username or password are incorrect")
    else:
        return {'user_id': user.id, 'username': user.username}


users_bp = Blueprint('users_bp', url_prefix='/users')
users_bp.add_route(UsersListResource.as_view(), '/', methods=['POST'])

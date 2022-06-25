"""Deeper 2022, All Rights Reserved
"""
from sanic import Request
from sanic_jwt.exceptions import AuthenticationFailed
from users.models import User


async def authenticate(request: Request):
    """
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        raise AuthenticationFailed('Missing username or password')

    async with request.ctx.session.begin():
        user = await User.get(username=username)
        
    if user is None or password != user.password:
        raise AuthenticationFailed("Username or password are incorrect")
    else:
        return dict(user)
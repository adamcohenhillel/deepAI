"""Deeper 2022, All Rights Reserved
"""
from sanic import Request
from sanic_jwt.exceptions import AuthenticationFailed
from api.users.models import User
from sqlalchemy.future import select


async def authenticate(request: Request):
    """Authentricate user based on username and password
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not (username or password):
        raise AuthenticationFailed('Missing username or password')

    async with request.ctx.session.begin():
        query = select(User).where(User.username == username)
        result = await request.ctx.session.execute(query)
        user: User = result.scalars().first()
        
    if user is None or password != user.password:
        raise AuthenticationFailed("Username or password are incorrect")
    else:
        return {'user_id': user.id, 'username': user.username}
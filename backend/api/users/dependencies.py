
"""Deeper 2022, All Rights Reserved
"""
from datetime import datetime, timedelta
import logging

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User
from db.dependencies import get_db_session
from settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/users/auth')


async def authenticated_user(
    db_session: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Endpoint Dependency for authenticated user with a token

    :param db_session: Inject db session dependency
    :param token: Inject token from the http header
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as e:
        logging.exception(e)
        raise credentials_exception
        
    username: str = payload.get('sub')
    if not username:
        raise credentials_exception

    query = await db_session.execute(select(User).where(User.username==username))
    user: User = query.scalars().first()
    if not user:
        raise credentials_exception

    return user


def create_access_token(data: dict, expiration: timedelta | None = None) -> str:
    """Create a JWT Access token to the api

    :param data: Data to store in the token, username for example
    :param expiration: How long the token will be valid for?

    :return: The JWT Token
    """
    to_encode = data.copy()
    now = datetime.utcnow()
    to_encode['exp'] = now + expiration if expiration else now + timedelta(minutes=15)
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

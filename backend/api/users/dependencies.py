
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# TODO: move to settings:
SECRET_KEY = 'change-me-adam-please'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def authenticated_user(
    db_session: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print(f'***** 1')
        logging.exception(e)
        raise credentials_exception
        
    username: str = payload.get('sub')
    if not username:
        print('***** 2')
        raise credentials_exception

    query = await db_session.execute(select(User).where(User.username==data.username))
    user: User = query.scalars().first()
    if not user:
        print('***** 3')
        raise credentials_exception

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

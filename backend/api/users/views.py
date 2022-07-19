"""Deeper 2022, All Rights Reserved
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.schemas import UserSchema
from db.models.user import User
from db.dependencies import get_db_session
from api.users.dependencies import authenticated_user, create_access_token


users_router = APIRouter()


@users_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserSchema,
    db_session: AsyncSession = Depends(get_db_session)
):
    """Create a new user
    """
    db_session.add(User(username=user.username, password=user.password))
    return {'message': 'Created'}


@users_router.post('/token')
async def login_for_access_token(
    db_session: AsyncSession = Depends(get_db_session),
    data: OAuth2PasswordRequestForm = Depends()
):
    """
    """
    query = await db_session.execute(select(User).where(User.username==data.username))
    user: User = query.scalars().first()
    verfied = user.verify_password(data.password) if user else False

    if not verfied:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=timedelta(minutes=30)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@users_router.get('/whoami')
async def read_users_me(current_user: User = Depends(authenticated_user)):
    """
    """
    return current_user

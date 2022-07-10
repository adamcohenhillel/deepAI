"""Deeper 2022, All Rights Reserved
"""
from typing import Dict
from sqlalchemy.future import select
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.schemas import UserSchema
from db.models.user import User
from db.session import get_db_session

users_router = APIRouter()

@users_router.post('/')
async def create_new_user(
    user: UserSchema,
    session: AsyncSession = Depends(get_db_session)
):
    """Create a new user
    """
    session.add(User(username=user.username, password=user.password))
    return {'message': 'Created'}

"""Deeper 2022, All Rights Reserved
"""
import re
from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, validator

from api.dependencies import authenticated_user, create_access_token
from db.models.user import User
from db.dependencies import get_db_session, get_neo4j_connector
from db.neo4j.entities import UserNode


users_router = APIRouter()


class UserInSchema(BaseModel):
    """Schema for getting user data from the client
    """
    username: str
    password: str

    @validator('password')
    def strong_password(cls, value, values):
        regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
        if not regex.search(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password too week, minimum eight characters, at least one letter and one number'
            )
        return value


class UserOutSchema(BaseModel):
    """Schema for returning user object to the client
    """
    id: int
    username: str

    class Config:
        orm_mode = True


@users_router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserInSchema,
    db_session: AsyncSession = Depends(get_db_session),
    neo4j_connector = Depends(get_neo4j_connector),
):
    """Create a new user (creates sql entry and a graph node)

    :param user: User details
    """
    new_user = User(username=user.username, password=user.password)
    db_session.add(new_user)
    await db_session.commit()
    with neo4j_connector.use_session() as session:
        session.write_transaction(UserNode.create, user_id=new_user.id)
    return {'message': 'Created'}


@users_router.post('/auth')
async def login_for_access_token(
    db_session: AsyncSession = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Authenticate user given a username and a password

    :param db_session: Inject db session dependency
    :param form_data: A username/password form must be given
    """
    query = await db_session.execute(select(User).where(User.username==form_data.username))
    user: User = query.scalars().first()
    verfied = user.verify_password(form_data.password) if user else False

    if not verfied:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data={'sub': user.username}, expiration=timedelta(minutes=30))
    return {'access_token': access_token, 'token_type': 'bearer'}


@users_router.get('/whoami', response_model=UserOutSchema)
async def whoami(user: User = Depends(authenticated_user)):
    """Test endpoint that depends on authenticated user
    """
    return user

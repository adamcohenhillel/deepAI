"""Deeper 2022, All Rights Reserved
"""
import re
from fastapi import HTTPException, status

from pydantic import BaseModel, validator


class UserInSchema(BaseModel):
    """
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
    """
    """
    id: int
    username: str

    class Config:
        orm_mode = True

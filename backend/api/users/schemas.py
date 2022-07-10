"""Deeper 2022, All Rights Reserved
"""
import re

from pydantic import BaseModel, validator


class UserSchema(BaseModel):
    """
    """
    username: str
    password: str

    @validator('password')
    def strong_password(cls, value, values):
        regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
        if not regex.search(value):
            raise ValueError('Password too week, minimum eight characters, at least one letter and one number')
        return value
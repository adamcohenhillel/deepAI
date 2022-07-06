"""Deeper 2022, All Rights Reserved
"""
import re
from dataclasses import dataclass
from typing import Any

from sanic.exceptions import InvalidUsage


@dataclass
class UserSchema:
    """
    """
    username: str
    password: str

    def __setattr__(self, attr: str, value: Any) -> None:
        """Validating the schema

        :param attr: schema attribute key
        :param value: schema attribute value
        """
        if attr == 'password':
            regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
            if not regex.search(value):
                raise InvalidUsage('Password too week, minimum eight characters, at least one letter and one number')
        self.__dict__[attr] = value
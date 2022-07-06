"""Deeper 2022, All Rights Reserved
"""
import os
from typing import Type, Union

from sanic.config import Config

class _AppConfig(Config):
    FALLBACK_ERROR_FORMAT = 'json'
    SANIC_JWT_SECRET = 'SecretShhhh'


class DevConfig(_AppConfig):
    DEBUG = True
    DATABASE_URI = 'sqlite+aiosqlite:////Users/adamcohenhillel/Desktop/projects/deeper/test.db'


class ProdConfig(_AppConfig):
    DATABASE_URI = 'postgresql+asyncpg://postgres:12345678@localhost/postgres'



def get_current_config():
    """Returns the config class to use
    """
    return DevConfig() if os.environ.get('DEV_MODE') else ProdConfig()

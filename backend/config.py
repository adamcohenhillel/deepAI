"""Deeper 2022, All Rights Reserved
"""
from sanic.config import Config

class AppConfig(Config):
    DEBUG = True
    FALLBACK_ERROR_FORMAT = 'json'
    SQLALCHEMY_DATABASE_URI = 'sqlite+aiosqlite:////Users/adamcohenhillel/Desktop/projects/deeper/test.db'

"""Deeper 2022, All Rights Reserved
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    workers_count: int = 1  # quantity of workers for uvicorn
    reload: bool = False  # Enable uvicorn reloading
    db_echo: bool = False
    
    # Current environment
    environment: str = "dev"
    db_url = 'postgresql+asyncpg://postgres:postgrespw@localhost:5433/postgres'

    neo4j_uri = 'bolt://localhost:7687'
    neo4j_user = 'neo4j'
    neo4j_password = '12345678'

    redis_url = 'redis://localhost:6379/0'

    class Config:
        env_file = ".env"
        env_prefix = "DEEPER2_"
        env_file_encoding = "utf-8"


settings = Settings()

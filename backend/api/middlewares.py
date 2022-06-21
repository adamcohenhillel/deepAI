from typing import Any
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.ext import Base
from core.neo4j.connector import Neo4jDBConnector
from api.users.models import User


engine = create_async_engine('sqlite+aiosqlite:////Users/adamcohenhillel/Desktop/projects/deeper/test.db', echo=True)
_base_model_session_ctx: ContextVar = ContextVar("session")


async def create_db_engine(app: Any, loop: Any) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # DELETE
        await conn.run_sync(Base.metadata.create_all)

    # DELETE:
    async_session = sessionmaker(engine, AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            session.add_all([User(username='admin', password='12345678')])
            await session.commit()


async def inject_session(request: Any) -> None:
    request.ctx.session = sessionmaker(engine, AsyncSession, expire_on_commit=False)()
    request.ctx.neo4j = Neo4jDBConnector("bolt://localhost:7687", "neo4j", "12345678")
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


async def close_session(request: Any, response: Any) -> None:
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()

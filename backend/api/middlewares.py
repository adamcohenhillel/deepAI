from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from api.users.models import User
from core.ext import Base

bind = create_async_engine('sqlite+aiosqlite:////Users/adamcohenhillel/Desktop/projects/deeper/test.db', echo=True)
_base_model_session_ctx = ContextVar("session")

async def inject_session(request):
    request.ctx.session = sessionmaker(bind, AsyncSession, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()
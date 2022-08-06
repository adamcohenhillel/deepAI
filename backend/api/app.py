"""Deeper 2022, All Rights Reserved
"""
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.routing import APIRouter

from api.routes.users import users_router
from api.routes.deeprequests import deeprequests_router
from api.routes.rooms import rooms_router
from api.lifetime import register_shutdown_event, register_startup_event
from api.exception_handlers import register_exception_handlers


def get_app() -> FastAPI:
    """Get API app
    """
    app = FastAPI(
        title="deeper.",
        description="Skip this for now",
        # version=metadata.version("deeper2"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)
    register_exception_handlers(app)

    api_router = APIRouter()
    api_router.include_router(users_router, prefix='/users', tags=['users'])
    api_router.include_router(deeprequests_router, prefix='/deeprequests', tags=['users'])
    api_router.include_router(rooms_router, prefix='/rooms', tags=['users'])

    app.include_router(router=api_router, prefix='/api')

    return app

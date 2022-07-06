"""Deeper 2022, All Rights Reserved
"""
from sanic import Sanic, Blueprint
from sanic.exceptions import SanicException
from sanic_jwt import Initialize
from sqlalchemy.exc import IntegrityError

from config import get_current_config
from api.deeprequest.views import deeprequest_bp
from api.users.views import users_bp
from api.users.views import authenticate
from api.middlewares import inject_session, close_session, create_db_engine
from api import exception_handlers 


def create_app() -> Sanic:
    """Create a new Sanic app instance
    """
    app = Sanic(__name__, config=get_current_config())

    ########################
    ##     BLUEPRINTS     ##
    api_blueprints = Blueprint.group(
        deeprequest_bp,
        users_bp,

        version='v1'
    )
    app.blueprint(api_blueprints)
    
    app.register_listener(create_db_engine, "after_server_start")
    app.register_middleware(inject_session, "request")
    app.register_middleware(close_session, "response")
    app.error_handler.add(Exception, exception_handlers.default_error_handler)
    app.error_handler.add(IntegrityError, exception_handlers.integrity_error_handler)
    app.error_handler.add(SanicException, exception_handlers.sanic_http_errors_handler)

    Initialize(app, authenticate=authenticate, url_prefix='/v1/auth', secret='kukuk')
    return app

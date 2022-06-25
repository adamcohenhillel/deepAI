"""Deeper 2022, All Rights Reserved
"""
from sanic import Sanic, Blueprint
from sanic_ext.exceptions import ValidationError
from sanic_jwt import Initialize
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from api.deeprequest.views import deeprequest_bp
from api.users.views import users_bp
from api.users.authenticate import authenticate
from api.middlewares import inject_session, close_session, create_db_engine
from api import exception_handlers 


def create_app():
    """
    """
    app = Sanic(__name__, config=AppConfig())

    ########################
    ##     BLUEPRINTS     ##
    api_blueprints = Blueprint.group(
        deeprequest_bp,
        users_bp,

        url_prefix='/api',
        version='v1'
    )
    app.blueprint(api_blueprints)
    
    app.register_listener(create_db_engine, "after_server_start")
    app.register_middleware(inject_session, "request")
    app.register_middleware(close_session, "response")
    app.error_handler.add(Exception, exception_handlers.catch_anything)
    app.error_handler.add(IntegrityError, exception_handlers.catch_integrity_error)
    app.error_handler.add(ValidationError, exception_handlers.catch_validation_error)

    Initialize(app, authenticate=authenticate)
    return app

"""Deeper 2022, All Rights Reserved
"""
from sanic import Sanic, Blueprint
from sanic_jwt import initialize

from config import AppConfig
from core.neo4j.connector import Neo4jDBConnector
from api.deeprequest.views import deeprequest_bp
from api.users.views import users_bp
from api.middlewares import inject_session, close_session
# from api.users.views import users_bp

from api.users.models import User


# ./server.py




def create_app():
    """
    """
    app = Sanic(__name__, config=AppConfig())

    # db.init_app(app)
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    #     # Create a test user for now TODO: Delete ME!
    #     db.session.add(User(username='admin', password='12345678'))
    #     db.session.commit()
    
    # initialize(app, authenticate=authenticate)

    app.ctx.neo4j = Neo4jDBConnector("bolt://localhost:7687", "neo4j", "12345678")

    ########################
    ##     BLUEPRINTS     ##
    api_blueprints = Blueprint.group(deeprequest_bp, users_bp, url_prefix='/api', version='v1')
    app.blueprint(api_blueprints)
    
    app.register_middleware(inject_session, "request")
    app.register_middleware(close_session, "response")
    return app

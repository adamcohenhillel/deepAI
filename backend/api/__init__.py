"""Deeper 2022, All Rights Reserved
"""
import os

from flask import Flask

from core.neo4j.connector import Neo4jDBConnector
from core.ext import db, jwt
from api.deeprequest.views import deeprequest_bp
from api.users.views import users_bp
from api.errors.handlers import errors_handlers_bp
from api.users.models import User
from worker import create_celery_instance


def create_app():
    """
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object('config.TestConfig' if os.getenv('TEST_MODE') else 'config.ProdConfig')

    jwt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create a test user for now TODO: Delete ME!
        db.session.add(User(username='admin', password='12345678'))
        db.session.commit()
    
    app.worker = create_celery_instance()
    app.neo4j = Neo4jDBConnector("bolt://localhost:7687", "neo4j", "12345678")

    ########################
    ##     BLUEPRINTS     ##
    app.register_blueprint(errors_handlers_bp)
    app.register_blueprint(deeprequest_bp, url_prefix='/api/v1/deeprequest')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    return app

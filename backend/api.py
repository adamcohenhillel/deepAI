"""Adam Cohen Hillel 2022, All Rights Reserved
"""
import os

from flask import Flask

from core.ext import db, jwt
from api.matchmaker.views import matchmaker_bp
from api.users.views import users_bp
from api.errors.handlers import errors_handlers_bp
from api.users.models import User

def create_app():
    """
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    test_mode = os.getenv('TEST_MODE') or False
    if test_mode:
        app.config.from_object('config.APITestConfig')
    else:
        app.config.from_object('config.APIProdConfig')


    jwt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create a test user for now TODO: Delete ME!
        db.session.add(User(username='admin', password='12345678'))
        db.session.commit()
    

    ########################
    ##     BLUEPRINTS     ##
    app.register_blueprint(errors_handlers_bp)
    app.register_blueprint(matchmaker_bp, url_prefix='/api/v1/matchmacker')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
"""Adam Cohen Hillel 2022, All Rights Reserved
"""
import os
import logging

from flask import Flask

from core.ext import db
from api.matchmaker.views import matchmaker_bp


def create_app():
    """
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    backend_test_mode = os.getenv('BACKEND_TEST_MODE') or False
    if backend_test_mode:
        app.config.from_object('config.APITestConfig')
    else:
        app.config.from_object('config.APIProdConfig')


    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(matchmaker_bp, url_prefix='/api/v1/matchmacker')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
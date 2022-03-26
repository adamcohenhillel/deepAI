"""
"""
from flask import Blueprint, request
from flask.views import MethodView


auth_bp = Blueprint('auth_bp', __name__)

class AccessTokensResource(MethodView):

    def get(self):
        pass

    def post(self):
        pass

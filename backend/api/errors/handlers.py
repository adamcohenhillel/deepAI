"""
"""
import logging

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from marshmallow.exceptions import ValidationError


errors_handlers_bp = Blueprint('errors_handlers_bp', __name__)


@errors_handlers_bp.app_errorhandler(ValidationError)
def handle_http_exceptions(exception: ValidationError):
    """Catch HTTP errors and return a json response
    """
    logging.exception(exception)
    return jsonify(exception.messages), 400


@errors_handlers_bp.app_errorhandler(HTTPException)
def handle_http_exceptions(exception: HTTPException):
    """Catch HTTP errors and return a json response
    """
    logging.exception(exception)
    return jsonify(msg=exception.description), exception.code


@errors_handlers_bp.app_errorhandler(Exception)
def handle_generic_exception(exception: Exception):
    """Catch any exception in the api and return a json response
    """
    logging.exception(exception)
    return jsonify(msg='Server Error'), 500

"""Deeper 2022, All Rights Reserved
"""
import logging
from sanic import Request
from sanic.response import json, HTTPResponse
from sanic.exceptions import SanicException
from sqlalchemy.exc import IntegrityError


async def integrity_error_handler(_: Request, exception: IntegrityError) -> HTTPResponse:
    """
    """
    logging.exception(exception)
    return json(body={'message': 'Resource already exists'}, status=400)


async def sanic_http_errors_handler(_: Request, exception: SanicException) -> HTTPResponse:
    """
    """
    logging.exception(exception)
    return json(body={'message': exception.args}, status=exception.status_code)


async def default_error_handler(_: Request, exception: Exception) -> HTTPResponse:
    """High level exception handler for all exceptions
    """
    logging.exception(exception)
    return json(body={'message': 'Unhandled Internal Server Error'}, status=500)

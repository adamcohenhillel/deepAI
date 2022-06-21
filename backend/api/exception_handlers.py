"""Deeper 2022, All Rights Reserved
"""
import logging
from sanic.response import json


async def catch_integrity_error(request, exception):
    """
    """
    logging.exception(exception)
    return json(body={'message': 'Resource exists already'}, status=400)


async def catch_anything(request, exception):
    """High level exception handler for all exceptions
    """
    logging.exception(exception)
    return json(body={'message': 'Unhandled Internal Server Error'}, status=500)
import logging
from sanic.response import json


async def catch_integrity_error(request, exception):
    logging.info('sdsdfsdfdsfsd')
    return json(body={'message': 'Resource exists already'}, status=400)

async def catch_anything(request, exception):
    """High level exception handler for all exceptions
    """
    return json(body={'message': 'Unhandled Internal Server Error'}, status=500)
"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from marshmallow import Schema, fields


class MatchRequestSchema(Schema):
    """
    """
    raw_request = fields.String(required=True)

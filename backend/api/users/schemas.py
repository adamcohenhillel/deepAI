"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from marshmallow import Schema, fields


class UserSchema(Schema):
    """
    """
    username = fields.String(required=True)
    password = fields.String(required=True)

"""Deeper 2022, All Rights Reserved
"""
from pydantic import BaseModel


class DeepRequestSchema(BaseModel):
    deep_request: str

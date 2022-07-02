"""Deeper 2022, All Rights Reserved
"""
import pytest
from api import create_app


@pytest.fixture
def api_app():
    return create_app()

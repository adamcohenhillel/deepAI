"""Deeper 2022, All Rights Reserved
"""
import pytest

from sanic import Sanic
from tests.fixtures import api_app
    

async def test_get_all_users(api_app):
    _, response = await api_app.asgi_client.post(
        '/v1/users',
        json={'password': '1234', 'username': 'banana'}
    )
    assert response.status == 201
    assert response.json == {'message': 'Created'}


class TestUserAuthentication:

    def test_authentication_success(self):
        pass

    def test_authentication_bad_username(self):
        pass

    def test_authentication_bad_password(self):
        pass

    def test_authentication_bad_body_schema(self):
        pass

    def test_authentication_no_body_schema(self):
        pass
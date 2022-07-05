"""Deeper 2022, All Rights Reserved
"""
import pytest

from tests.fixtures import generic_test_setup, GenericTestSetup
    

async def test_get_all_users(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post(
        '/v1/users',
        json={'password': '1234', 'username': 'banana'}
    )
    assert response.status == 201
    assert response.json == {'message': 'Created'}


async def test_authentication_success(generic_test_setup: GenericTestSetup) -> None:
    api_app, database_session = generic_test_setup

    _, response = await api_app.asgi_client.post(
        '/v1/auth',
        json={'password': '12345678', 'username': 'test_user'}
    )
    assert response.status == 200
    assert 'access_token' in response.json


    # async def test_authentication_bad_username(self):
    #     pass

    # async def test_authentication_bad_password(self):
    #     pass

    # async def test_authentication_bad_body_schema(self):
    #     pass

    # async def test_authentication_no_body_schema(self):
    #     pass
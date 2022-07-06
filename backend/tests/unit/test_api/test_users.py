"""Deeper 2022, All Rights Reserved
"""
from tests.fixtures import generic_test_setup, GenericTestSetup
    

async def test_create_new_user_success(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post(
        '/v1/users',
        json={'password': 'Aa12345678@', 'username': 'banana'}
    )
    assert response.status == 201
    assert response.json == {'message': 'Created'}


async def test_create_new_user_existing_username(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post(
        '/v1/users',
        json={'password': 'Aa12345678@', 'username': 'test_user'}
    )
    assert response.status == 400


async def test_create_new_user_week_password(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post(
        '/v1/users',
        json={'password': 'week', 'username': 'banana'}
    )
    assert response.status == 400


async def test_authentication_success(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post('/v1/auth', json={'password': 'Aa12345678!', 'username': 'test_user'})
    assert 'access_token' in response.json


async def test_authentication_bad_username(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post('/v1/auth', json={'password': '12345678', 'username': 'notexists'})
    assert response.status == 401


async def test_authentication_bad_password(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post('/v1/auth', json={'password': 'badpass', 'username': 'test_user'})
    assert response.status == 401


async def test_authentication_bad_body_schema(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post('/v1/auth', json={'notpassword': '12345678', 'username': 'test_user'})
    assert response.status == 401


async def test_authentication_no_body_schema(generic_test_setup: GenericTestSetup) -> None:
    api_app, _ = generic_test_setup
    _, response = await api_app.asgi_client.post('/v1/auth')
    assert response.status == 400

"""Deeper 2022, All Rights Reserved
"""
from typing import Tuple
from httpx import AsyncClient


async def test_create_new_user_success(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users',
        json={'password': 'Aa12345678@', 'username': 'banana'}
    )
    print(response.__dict__)
    assert response.status_code == 201
    assert response.json() == {'message': 'Created'}


async def test_create_new_user_existing_username(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users',
        json={'password': 'Aa12345678@', 'username': 'test_user'}
    )
    print(response.json())
    assert response.status_code == 409


async def test_create_new_user_week_password(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users',
        json={'password': 'week', 'username': 'banana'}
    )
    assert response.status_code == 400
    assert response.json()['detail'].startswith('Password too week')


async def test_create_new_user_bad_schema(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users',
        json={'password': 'week', 'woops': 'banana'}
    )
    assert response.status_code == 400


async def test_authentication_success(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users/auth',
        data={'password': 'Aa12345678!', 'username': 'test_user'}
    )
    assert 'access_token' in response.json()


async def test_authentication_bad_username(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users/auth',
        data={'password': 'Aa12345678!', 'username': 'ayeeayeeayee'}
    )
    assert response.status_code == 401


async def test_authentication_bad_password(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users/auth',
        data={'password': 'oopsi', 'username': 'test_user'}
    )
    assert response.status_code == 401


async def test_authentication_bad_body_schema(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users/auth',
        data={'password': 'Aa12345678!', 'woopwoop': 'test_user'}
    )
    assert response.status_code == 422


async def test_authentication_no_body_schema(client: AsyncClient) -> None:
    response = await client.post(
        '/api/users/auth'
    )
    assert response.status_code == 422


async def test_whoami_success(client_and_token: Tuple[AsyncClient, str]) -> None:
    client, token = client_and_token
    response = await client.get(
        '/api/users/whoami',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert 'test_user' == response.json()['username']


async def test_whoami_bad_token(client: AsyncClient) -> None:
    response = await client.get(
        '/api/users/whoami',
        headers={'Authorization': f'Bearer ooppsii'}
    )
    assert response.status_code == 401


async def test_whoami_no_token(client: AsyncClient) -> None:
    response = await client.get(
        '/api/users/whoami',
    )
    assert response.status_code == 401

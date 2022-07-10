"""Deeper 2022, All Rights Reserved
"""

async def test_create_new_user_success(client) -> None:
    response = await client.post(
        '/api/users/',
        json={'password': 'Aa12345678@', 'username': 'banana'}
    )
    print(response.__dict__)
    assert response.status_code == 200
    assert response.json() == {'message': 'Created'}


# def test_create_new_user_existing_username(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = api_app.test_client.post(
#         '/v1/users',
#         json={'password': 'Aa12345678@', 'username': 'test_user'}
#     )
#     assert response.status == 400


# async def test_create_new_user_week_password(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = await api_app.asgi_client.post(
#         '/v1/users',
#         json={'password': 'week', 'username': 'banana'}
#     )
#     assert response.status == 400


# async def test_create_new_user_bad_schema(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = await api_app.asgi_client.post(
#         '/v1/users',
#         json={'password': 'week', 'woops': 'banana'}
#     )
#     assert response.status == 400


# async def test_authentication_success(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = await api_app.asgi_client.post('/v1/auth', json={'password': 'Aa12345678!', 'username': 'test_user'})
#     assert 'access_token' in response.json


# async def test_authentication_bad_username(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = await api_app.asgi_client.post('/v1/auth', json={'password': '12345678', 'username': 'notexists'})
#     assert response.status == 401


# async def test_authentication_bad_password(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = await api_app.asgi_client.post('/v1/auth', json={'password': 'badpass', 'username': 'test_user'})
#     assert response.status == 401


# async def test_authentication_bad_body_schema(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = await api_app.asgi_client.post('/v1/auth', json={'notpassword': '12345678', 'username': 'test_user'})
#     assert response.status == 401


# async def test_authentication_no_body_schema(generic_test_setup: GenericTestSetup) -> None:
#     api_app, _, _ = generic_test_setup
#     _, response = await api_app.asgi_client.post('/v1/auth')
#     assert response.status == 400
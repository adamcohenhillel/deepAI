# """Deeper 2022, All Rights Reserved
# """
# from tests.fixtures import generic_test_setup, GenericTestSetup
    

# # async def test_create_new_deep_request(generic_test_setup: GenericTestSetup) -> None:
# #     api_app, _, access_token = generic_test_setup
# #     _, response = await api_app.asgi_client.post(
# #         '/v1/deeprequest',
# #         headers={'Authorization': f'Bearer {access_token}'},
# #         json={'deep_request': 'This is something deep'}
# #     )
# #     assert response.status == 201
# #     assert isinstance(response.json['node'], int)

"""Deeper 2022, All Rights Reserved
"""
from tests.fixtures import api_app
    
class TestUsersAPI:
    """Tests the api.users application
    """

    def test_get_all_users(self, api_app):
        # request, response = sanic_app.test_client.post(
        #     '/v1/users',
        #     json={'password': '1234', 'username': 'banana'}
        # )
        pass
        # assert response.body == b"foo"


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
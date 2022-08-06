"""Deeper 2022, All Rights Reserved
"""
    

async def test_create_new_deep_request(client) -> None:
    response = await client.post(
        '/api/deeprequests/',
        # headers={'Authorization': f'Bearer {access_token}'},
        json={'deep_request': 'This is something deep'}
    )
    assert response.status_code == 200
    assert isinstance(response.json()['node'], int)


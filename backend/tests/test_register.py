from fastapi import testclient

from backend.tests import conftest


def test_ok(client: testclient.TestClient):
    password = conftest.fake.password()
    response = client.post('/api/v1/auth/register', json={
        'email': conftest.fake.email(),
        'name': conftest.fake.name(),
        'password': password,
        'password_check': password,
    })

    assert response.status_code == 201
    data = response.json()

    assert data['status'] == 'success'

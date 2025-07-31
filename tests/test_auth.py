import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_register_and_login(client):
    client.post('/register', json={"email": "test@example.com", "password": "123456"})
    response = client.post('/login', json={"email": "test@example.com", "password": "123456"})
    assert response.status_code == 200
    assert "token" in response.get_json()
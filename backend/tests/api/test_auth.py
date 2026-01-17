def test_login(client):
    response = client.post("/token", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_fail(client):
    response = client.post("/token", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401

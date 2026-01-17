"""
Tests for authentication endpoints and edge cases.
"""


def test_login(client):
    response = client.post("/auth/token", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_fail(client):
    response = client.post("/auth/token", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Test login with non-existent username."""
    response = client.post("/auth/token", data={"username": "nonexistent", "password": "anypassword"})
    assert response.status_code == 401


def test_login_empty_username(client):
    """Test login with empty username."""
    response = client.post("/auth/token", data={"username": "", "password": "password123"})
    assert response.status_code == 422  # Validation error for empty username


def test_login_empty_password(client):
    """Test login with empty password."""
    response = client.post("/auth/token", data={"username": "admin", "password": ""})
    assert response.status_code == 422  # Validation error for empty password


def test_login_missing_credentials(client):
    """Test login with missing credentials."""
    response = client.post("/auth/token", data={})
    assert response.status_code == 422  # Validation error


def test_token_format(client):
    """Test that returned token is a valid JWT format."""
    response = client.post("/auth/token", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    # JWT tokens have three parts separated by dots
    assert len(token.split('.')) == 3


def test_access_protected_endpoint_with_valid_token(client, admin_token):
    """Test accessing protected endpoint with valid token."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200


def test_access_protected_endpoint_without_token(client):
    """Test that protected endpoints require authentication."""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_access_protected_endpoint_with_invalid_token(client):
    """Test accessing protected endpoint with invalid token."""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401


def test_access_protected_endpoint_with_malformed_header(client):
    """Test accessing protected endpoint with malformed auth header."""
    headers = {"Authorization": "InvalidFormat token"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401


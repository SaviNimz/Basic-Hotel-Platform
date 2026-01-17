"""
Tests for user management API endpoints.
"""

def test_get_current_user_me(client, admin_headers):
    """Test getting current user information."""
    response = client.get("/users/me", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert "id" in data


def test_create_user(client, admin_headers):
    """Test creating a new user."""
    response = client.post(
        "/users/",
        json={"username": "newuser", "password": "newpass123"},
        headers=admin_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert "password" not in data  
    assert "password_hash" not in data  # Hash should not be returned


def test_create_duplicate_user(client, admin_headers):
    """Test that creating a user with existing username fails."""
    # Create first user
    client.post(
        "/users/",
        json={"username": "duplicate", "password": "pass123"},
        headers=admin_headers
    )
    
    # Try to create duplicate
    response = client.post(
        "/users/",
        json={"username": "duplicate", "password": "pass456"},
        headers=admin_headers
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_get_users_list(client, admin_headers):
    """Test getting list of users."""
    # Create a few users
    for i in range(3):
        client.post(
            "/users/",
            json={"username": f"listuser{i}", "password": "pass123"},
            headers=admin_headers
        )
    
    response = client.get("/users/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  


def test_get_user_by_id(client, admin_headers):
    """Test getting a specific user by ID."""
    # Create a user
    create_res = client.post(
        "/users/",
        json={"username": "getbyid", "password": "pass123"},
        headers=admin_headers
    )
    user_id = create_res.json()["id"]
    
    # Get the user
    response = client.get(f"/users/{user_id}", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "getbyid"


def test_get_user_not_found(client, admin_headers):
    """Test getting non-existent user returns 404."""
    response = client.get("/users/9999", headers=admin_headers)
    assert response.status_code == 404


def test_update_user(client, admin_headers):
    """Test updating user information."""
    # Create a user
    create_res = client.post(
        "/users/",
        json={"username": "updateme", "password": "oldpass"},
        headers=admin_headers
    )
    user_id = create_res.json()["id"]
    
    # Update username
    update_res = client.put(
        f"/users/{user_id}",
        json={"username": "updated"},
        headers=admin_headers
    )
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["username"] == "updated"


def test_update_user_duplicate_username(client, admin_headers):
    """Test that updating username to existing one fails."""
    # Create two users
    user1 = client.post(
        "/users/",
        json={"username": "user1", "password": "pass123"},
        headers=admin_headers
    ).json()
    
    user2_id = client.post(
        "/users/",
        json={"username": "user2", "password": "pass123"},
        headers=admin_headers
    ).json()["id"]
    
    # Try to update user2's username to user1
    response = client.put(
        f"/users/{user2_id}",
        json={"username": "user1"},
        headers=admin_headers
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_delete_user(client, admin_headers):
    """Test deleting a user."""
    # Create a user
    create_res = client.post(
        "/users/",
        json={"username": "deleteme", "password": "pass123"},
        headers=admin_headers
    )
    user_id = create_res.json()["id"]
    
    # Delete the user
    delete_res = client.delete(f"/users/{user_id}", headers=admin_headers)
    assert delete_res.status_code == 200
    
    # Verify it's deleted
    get_res = client.get(f"/users/{user_id}", headers=admin_headers)
    assert get_res.status_code == 404


def test_delete_user_not_found(client, admin_headers):
    """Test deleting non-existent user returns 404."""
    response = client.delete("/users/9999", headers=admin_headers)
    assert response.status_code == 404


def test_unauthorized_access_without_token(client):
    """Test that endpoints require authentication."""
    response = client.get("/users/")
    assert response.status_code == 401

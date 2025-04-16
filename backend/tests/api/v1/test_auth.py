import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models import AdminUser
from app.core.security import hash_password, create_access_token
from app import schemas

API_V1_STR = "/api/v1"

def test_admin_login_success(client: TestClient, test_admin_user: AdminUser):
    """Test successful admin login."""
    login_data = {
        "username": test_admin_user.username,
        "password": test_admin_user.raw_password,
    }
    response = client.post(f"{API_V1_STR}/admin/login", json=login_data)
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

def test_admin_login_wrong_password(client: TestClient, test_admin_user: AdminUser):
    """Test admin login with incorrect password."""
    login_data = {
        "username": test_admin_user.username,
        "password": "wrongpassword",
    }
    response = client.post(f"{API_V1_STR}/admin/login", json=login_data)
    assert response.status_code == 401
    content = response.json()
    assert content["detail"] == "Incorrect username or password"
    assert "WWW-Authenticate" in response.headers

def test_admin_login_nonexistent_user(client: TestClient):
    """Test admin login with a username that does not exist."""
    login_data = {
        "username": "nonexistentuser",
        "password": "somepassword",
    }
    response = client.post(f"{API_V1_STR}/admin/login", json=login_data)
    assert response.status_code == 401
    content = response.json()
    assert content["detail"] == "Incorrect username or password"

# --- Helper function to get token ---
def get_admin_auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    login_data = {"username": username, "password": password}
    response = client.post(f"{API_V1_STR}/admin/login", json=login_data)
    response.raise_for_status() # Raise exception for non-200 status
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- Protected Endpoint Tests --- 

def test_read_admin_me_success(client: TestClient, test_admin_user: AdminUser):
    """Test accessing protected /admin/me endpoint with valid token."""
    headers = get_admin_auth_headers(
        client, test_admin_user.username, test_admin_user.raw_password
    )
    response = client.get(f"{API_V1_STR}/admin/me", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert content["username"] == test_admin_user.username
    assert content["id"] == test_admin_user.id

def test_read_admin_me_no_token(client: TestClient):
    """Test accessing protected endpoint without a token."""
    response = client.get(f"{API_V1_STR}/admin/me")
    assert response.status_code == 401 # Depends on OAuth2PasswordBearer default
    assert "Not authenticated" in response.json().get("detail", "")

def test_read_admin_me_invalid_token(client: TestClient):
    """Test accessing protected endpoint with an invalid/malformed token."""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get(f"{API_V1_STR}/admin/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json().get("detail", "")

def test_read_admin_me_expired_token(client: TestClient, test_admin_user: AdminUser):
    """Test accessing protected endpoint with an expired token."""
    # Create an expired token manually
    expired_token = create_access_token(
        test_admin_user.username, expires_delta=timedelta(minutes=-5)
    )
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get(f"{API_V1_STR}/admin/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json().get("detail", "") 
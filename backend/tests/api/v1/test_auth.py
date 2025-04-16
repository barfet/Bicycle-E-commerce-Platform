import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import AdminUser
from app.core.security import hash_password
from app import schemas

API_V1_STR = "/api/v1"

@pytest.fixture(scope="function")
def test_admin_user(db_session: Session) -> AdminUser:
    """Fixture to create a test admin user in the database for each test."""
    username = "testloginadmin"
    password = "testpassword"
    hashed = hash_password(password)
    user = AdminUser(username=username, password_hash=hashed)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    # Add the raw password for test usage
    user.raw_password = password 
    return user

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
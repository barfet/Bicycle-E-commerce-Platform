import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.models import ProductType, AdminUser # Import models
from app.schemas import ProductTypeCreate, ProductTypeUpdate # Import schemas
from app.core.security import hash_password # For creating admin user

# Helper from test_auth (or move to a shared conftest)
from tests.api.v1.test_auth import get_admin_auth_headers, API_V1_STR

ADMIN_ENDPOINT = f"{API_V1_STR}/admin/product-types"

@pytest.fixture(scope="function")
def test_product_type_id_db(db_session: Session) -> int:
    """Fixture to create a product type directly in DB and return its ID."""
    pt_in = ProductTypeCreate(name="Test Bike Type DB", description="For testing")
    pt = crud.create_product_type(db=db_session, product_type_in=pt_in)
    return pt.id

# Test Auth Requirement (applied to one endpoint, assumed for others due to Depends)
def test_read_product_types_unauthenticated(client: TestClient):
    response = client.get(ADMIN_ENDPOINT)
    assert response.status_code == 401 # Expect unauthorized

# Test CRUD Operations
def test_create_product_type_api(client: TestClient, db_session: Session, test_admin_user: AdminUser):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    pt_data = {"name": "API Created Bike", "description": "Created via API test"}
    response = client.post(ADMIN_ENDPOINT, headers=headers, json=pt_data)
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == pt_data["name"]
    assert content["description"] == pt_data["description"]
    assert "id" in content

    # Verify it exists in DB
    db_obj = db_session.get(ProductType, content["id"])
    assert db_obj is not None
    assert db_obj.name == pt_data["name"]

def test_create_product_type_duplicate_name(client: TestClient, test_product_type_id_db: int, test_admin_user: AdminUser, db_session: Session):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    # Fetch the object within the test's session
    test_product_type_db = db_session.get(ProductType, test_product_type_id_db)
    assert test_product_type_db is not None
    # Try creating with the same name as the fixture
    pt_data = {"name": test_product_type_db.name, "description": "Duplicate attempt"}
    response = client.post(ADMIN_ENDPOINT, headers=headers, json=pt_data)
    # Expecting IntegrityError to be caught and return 409 Conflict
    assert response.status_code == 409
    assert "already exists" in response.json().get("detail", "")

def test_read_product_types_api(client: TestClient, test_product_type_id_db: int, test_admin_user: AdminUser, db_session: Session):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    # Fetch the object within the test's session
    test_product_type_db = db_session.get(ProductType, test_product_type_id_db)
    assert test_product_type_db is not None
    response = client.get(ADMIN_ENDPOINT, headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) >= 1
    # Check if our test item is in the list
    found = any(item["id"] == test_product_type_db.id and item["name"] == test_product_type_db.name for item in content)
    assert found

def test_read_single_product_type_api(client: TestClient, test_product_type_id_db: int, test_admin_user: AdminUser, db_session: Session):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    # Fetch the object within the test's session
    test_product_type_db = db_session.get(ProductType, test_product_type_id_db)
    assert test_product_type_db is not None
    response = client.get(f"{ADMIN_ENDPOINT}/{test_product_type_db.id}", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == test_product_type_db.name
    assert content["description"] == test_product_type_db.description
    assert content["id"] == test_product_type_db.id

def test_read_single_product_type_not_found(client: TestClient, test_admin_user: AdminUser):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    response = client.get(f"{ADMIN_ENDPOINT}/99999", headers=headers) # Non-existent ID
    assert response.status_code == 404

def test_update_product_type_api(client: TestClient, test_product_type_id_db: int, test_admin_user: AdminUser):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    update_data = {"name": "Updated Bike Name", "description": "Updated Desc"}
    response = client.put(f"{ADMIN_ENDPOINT}/{test_product_type_id_db}", headers=headers, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["description"] == update_data["description"]
    assert content["id"] == test_product_type_id_db

def test_update_product_type_not_found(client: TestClient, test_admin_user: AdminUser):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    update_data = {"name": "Update Non Existent"}
    response = client.put(f"{ADMIN_ENDPOINT}/99999", headers=headers, json=update_data)
    assert response.status_code == 404

def test_delete_product_type_api(client: TestClient, test_product_type_id_db: int, test_admin_user: AdminUser, db_session: Session):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    response = client.delete(f"{ADMIN_ENDPOINT}/{test_product_type_id_db}", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == test_product_type_id_db

    # Verify it's deleted from DB
    db_obj = db_session.get(ProductType, test_product_type_id_db)
    assert db_obj is None

def test_delete_product_type_not_found(client: TestClient, test_admin_user: AdminUser):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    response = client.delete(f"{ADMIN_ENDPOINT}/99999", headers=headers) # Non-existent ID
    assert response.status_code == 404 
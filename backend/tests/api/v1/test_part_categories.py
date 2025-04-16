import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, models, schemas
from tests.api.v1.test_auth import get_admin_auth_headers, API_V1_STR # Reuse helper

ADMIN_ENDPOINT = f"{API_V1_STR}/admin/part-categories"

# Fixture to create a prerequisite ProductType
@pytest.fixture(scope="function")
def test_product_type_for_category(db_session: Session) -> models.ProductType:
    pt_in = schemas.ProductTypeCreate(name="Test Bike For Category", description="Prereq")
    return crud.create_product_type(db=db_session, product_type_in=pt_in)

# Fixture to create a PartCategory linked to the ProductType
@pytest.fixture(scope="function")
def test_part_category_db(db_session: Session, test_product_type_for_category: models.ProductType) -> models.PartCategory:
    pc_in = schemas.PartCategoryCreate(
        name="Frame",
        product_type_id=test_product_type_for_category.id,
        display_order=1
    )
    return crud.create_part_category(db=db_session, part_category_in=pc_in)

def test_create_part_category_api(
    client: TestClient, db_session: Session, test_admin_user: models.AdminUser, test_product_type_for_category: models.ProductType
):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    pc_data = {
        "name": "Wheels API",
        "product_type_id": test_product_type_for_category.id,
        "display_order": 2
    }
    response = client.post(ADMIN_ENDPOINT, headers=headers, json=pc_data)
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == pc_data["name"]
    assert content["product_type_id"] == pc_data["product_type_id"]
    assert content["display_order"] == pc_data["display_order"]
    assert "id" in content

    # Verify in DB
    db_obj = db_session.get(models.PartCategory, content["id"])
    assert db_obj is not None
    assert db_obj.name == pc_data["name"]

def test_create_part_category_invalid_product_type(client: TestClient, test_admin_user: models.AdminUser):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    pc_data = {"name": "Fork", "product_type_id": 99999} # Non-existent product type
    response = client.post(ADMIN_ENDPOINT, headers=headers, json=pc_data)
    assert response.status_code == 404 # Check if product type exists

def test_read_part_categories_unauthenticated(client: TestClient):
    response = client.get(ADMIN_ENDPOINT + "?product_type_id=1") # Need query param
    assert response.status_code == 401

def test_read_part_categories_missing_query_param(client: TestClient, test_admin_user: models.AdminUser):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    response = client.get(ADMIN_ENDPOINT, headers=headers)
    assert response.status_code == 400 # Check requirement for product_type_id
    assert "product_type_id' is required" in response.json().get("detail", "")

def test_read_part_categories_filtered(
    client: TestClient, test_admin_user: models.AdminUser, test_part_category_db: models.PartCategory
):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    product_type_id = test_part_category_db.product_type_id
    response = client.get(f"{ADMIN_ENDPOINT}?product_type_id={product_type_id}", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) >= 1
    # Check if our test item is in the list
    found = any(item["id"] == test_part_category_db.id and item["name"] == test_part_category_db.name for item in content)
    assert found
    # Check if items belong to the correct product type
    assert all(item["product_type_id"] == product_type_id for item in content)

def test_read_single_part_category_api(client: TestClient, test_admin_user: models.AdminUser, test_part_category_db: models.PartCategory):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    response = client.get(f"{ADMIN_ENDPOINT}/{test_part_category_db.id}", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == test_part_category_db.name
    assert content["id"] == test_part_category_db.id
    assert content["product_type_id"] == test_part_category_db.product_type_id

def test_update_part_category_api(client: TestClient, test_admin_user: models.AdminUser, test_part_category_db: models.PartCategory):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    update_data = {"name": "Updated Frame Name", "display_order": 10}
    response = client.put(f"{ADMIN_ENDPOINT}/{test_part_category_db.id}", headers=headers, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["display_order"] == update_data["display_order"]
    assert content["id"] == test_part_category_db.id
    assert content["product_type_id"] == test_part_category_db.product_type_id # Not changed

def test_delete_part_category_api(client: TestClient, test_admin_user: models.AdminUser, test_part_category_db: models.PartCategory, db_session: Session):
    headers = get_admin_auth_headers(client, test_admin_user.username, test_admin_user.raw_password)
    part_category_id = test_part_category_db.id
    response = client.delete(f"{ADMIN_ENDPOINT}/{part_category_id}", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == part_category_id

    # Verify deleted from DB
    db_obj = db_session.get(models.PartCategory, part_category_id)
    assert db_obj is None 
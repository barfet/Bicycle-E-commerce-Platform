import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_part_category
from app import crud, models
from app.schemas import PartCategoryCreate, PartOptionCreate, PartOptionUpdate

pytestmark = pytest.mark.asyncio


async def test_create_part_option(
    client: AsyncClient, db: AsyncSession, admin_user_headers: dict, test_product_type: models.ProductType
) -> None:
    # First, create a PartCategory to link the PartOption to
    part_category_in = PartCategoryCreate(
        name="Test Category for PartOption", product_type_id=test_product_type.id
    )
    part_category = await create_part_category(db=db, obj_in=part_category_in)

    part_option_in = {
        "name": "Test Part Option",
        "part_category_id": part_category.id,
        "base_price": 100.00,
        "is_in_stock": True,
    }
    response = await client.post(
        "/api/v1/admin/part-options/",
        headers=admin_user_headers,
        json=part_option_in,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == part_option_in["name"]
    assert content["part_category_id"] == part_option_in["part_category_id"]
    assert content["base_price"] == part_option_in["base_price"]
    assert content["is_in_stock"] == part_option_in["is_in_stock"]
    assert "id" in content


async def test_create_part_option_category_not_found(client: AsyncClient, admin_user_headers: dict) -> None:
    part_option_in = {
        "name": "Test Part Option Invalid Category",
        "part_category_id": 99999,  # Non-existent category ID
        "base_price": 50.00,
        "is_in_stock": False,
    }
    response = await client.post(
        "/api/v1/admin/part-options/",
        headers=admin_user_headers,
        json=part_option_in,
    )
    assert response.status_code == 404
    content = response.json()
    assert "Part Category not found" in content["detail"]


async def test_read_part_options(
    client: AsyncClient, db: AsyncSession, admin_user_headers: dict, test_product_type: models.ProductType
) -> None:
    # Create a PartCategory and a PartOption for testing
    part_category_in = PartCategoryCreate(
        name="Test Category for Reading", product_type_id=test_product_type.id
    )
    part_category = await create_part_category(db=db, obj_in=part_category_in)
    part_option_in = PartOptionCreate(
        name="Test Part Option Read",
        part_category_id=part_category.id,
        base_price=120.50,
        is_in_stock=True,
    )
    await crud.create_part_option(db=db, obj_in=part_option_in)

    # Test reading all options for the specific category
    response = await client.get(
        f"/api/v1/admin/part-options/?part_category_id={part_category.id}",
        headers=admin_user_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) >= 1
    assert content[0]["name"] == part_option_in.name
    assert content[0]["part_category_id"] == part_category.id


async def test_read_part_options_category_id_required(client: AsyncClient, admin_user_headers: dict) -> None:
    response = await client.get("/api/v1/admin/part-options/", headers=admin_user_headers)
    assert response.status_code == 400
    assert "part_category_id" in response.json()["detail"]


async def test_read_part_option(
    client: AsyncClient, db: AsyncSession, admin_user_headers: dict, test_product_type: models.ProductType
) -> None:
    # Create a PartCategory and a PartOption for testing
    part_category_in = PartCategoryCreate(
        name="Test Category for Specific Read", product_type_id=test_product_type.id
    )
    part_category = await create_part_category(db=db, obj_in=part_category_in)
    part_option_in = PartOptionCreate(
        name="Test Part Option Specific Read",
        part_category_id=part_category.id,
        base_price=150.00,
        is_in_stock=False,
    )
    part_option = await crud.create_part_option(db=db, obj_in=part_option_in)

    response = await client.get(
        f"/api/v1/admin/part-options/{part_option.id}",
        headers=admin_user_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == part_option_in.name
    assert content["id"] == part_option.id
    assert content["part_category_id"] == part_category.id
    assert content["base_price"] == part_option_in.base_price


async def test_read_part_option_not_found(client: AsyncClient, admin_user_headers: dict) -> None:
    response = await client.get("/api/v1/admin/part-options/99999", headers=admin_user_headers)
    assert response.status_code == 404


async def test_update_part_option(
    client: AsyncClient, db: AsyncSession, admin_user_headers: dict, test_product_type: models.ProductType
) -> None:
    # Create a PartCategory and a PartOption for testing
    part_category_in = PartCategoryCreate(
        name="Test Category for Update", product_type_id=test_product_type.id
    )
    part_category = await create_part_category(db=db, obj_in=part_category_in)
    part_option_in = PartOptionCreate(
        name="Original Part Option Name",
        part_category_id=part_category.id,
        base_price=200.00,
        is_in_stock=True,
    )
    part_option = await crud.create_part_option(db=db, obj_in=part_option_in)

    part_option_update_data = {
        "name": "Updated Part Option Name",
        "base_price": 250.50,
        "is_in_stock": False,
    }

    response = await client.put(
        f"/api/v1/admin/part-options/{part_option.id}",
        headers=admin_user_headers,
        json=part_option_update_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == part_option_update_data["name"]
    assert content["id"] == part_option.id
    assert content["part_category_id"] == part_category.id  # Should not change
    assert content["base_price"] == part_option_update_data["base_price"]
    assert content["is_in_stock"] == part_option_update_data["is_in_stock"]


async def test_update_part_option_not_found(client: AsyncClient, admin_user_headers: dict) -> None:
    part_option_update_data = {
        "name": "Non Existent Update",
        "base_price": 10.0,
        "is_in_stock": True,
    }
    response = await client.put(
        "/api/v1/admin/part-options/99999",
        headers=admin_user_headers,
        json=part_option_update_data,
    )
    assert response.status_code == 404


async def test_delete_part_option(
    client: AsyncClient, db: AsyncSession, admin_user_headers: dict, test_product_type: models.ProductType
) -> None:
    # Create a PartCategory and a PartOption for testing
    part_category_in = PartCategoryCreate(
        name="Test Category for Deletion", product_type_id=test_product_type.id
    )
    part_category = await create_part_category(db=db, obj_in=part_category_in)
    part_option_in = PartOptionCreate(
        name="Part Option to Delete",
        part_category_id=part_category.id,
        base_price=50.00,
        is_in_stock=True,
    )
    part_option = await crud.create_part_option(db=db, obj_in=part_option_in)

    response = await client.delete(
        f"/api/v1/admin/part-options/{part_option.id}",
        headers=admin_user_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == part_option_in.name
    assert content["id"] == part_option.id

    # Verify it's deleted
    deleted_option = await crud.get_part_option(db=db, id=part_option.id)
    assert deleted_option is None


async def test_delete_part_option_not_found(client: AsyncClient, admin_user_headers: dict) -> None:
    response = await client.delete("/api/v1/admin/part-options/99999", headers=admin_user_headers)
    assert response.status_code == 404 
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

from app.models import ProductType, PartCategory, PartOption

def test_create_product_type(db_session: Session):
    """Test creating a ProductType instance."""
    pt = ProductType(name="Bicycle", description="Standard bicycle")
    db_session.add(pt)
    db_session.commit()
    db_session.refresh(pt)

    assert pt.id is not None
    assert pt.name == "Bicycle"
    assert pt.description == "Standard bicycle"
    assert pt.created_at is not None
    assert pt.updated_at is not None

def test_product_type_name_unique(db_session: Session):
    """Test uniqueness constraint on ProductType name."""
    pt1 = ProductType(name="UniqueBike")
    db_session.add(pt1)
    db_session.commit()

    pt2 = ProductType(name="UniqueBike")
    db_session.add(pt2)
    with pytest.raises(IntegrityError):
        db_session.commit()

def test_create_part_category(db_session: Session):
    """Test creating a PartCategory linked to a ProductType."""
    pt = ProductType(name="Test Bike")
    db_session.add(pt)
    db_session.commit()
    db_session.refresh(pt)

    pc = PartCategory(name="Frame", product_type_id=pt.id, display_order=1)
    db_session.add(pc)
    db_session.commit()
    db_session.refresh(pc)

    assert pc.id is not None
    assert pc.name == "Frame"
    assert pc.product_type_id == pt.id
    assert pc.display_order == 1
    assert pc.product_type.name == "Test Bike"
    assert pt.part_categories[0].name == "Frame"

def test_create_part_option(db_session: Session):
    """Test creating a PartOption linked to a PartCategory."""
    pt = ProductType(name="Another Bike")
    pc = PartCategory(name="Wheels", product_type=pt)
    db_session.add_all([pt, pc])
    db_session.commit()
    db_session.refresh(pc)

    po = PartOption(
        name="29 inch",
        part_category_id=pc.id,
        base_price=Decimal("50.99"),
        is_in_stock=True
    )
    db_session.add(po)
    db_session.commit()
    db_session.refresh(po)

    assert po.id is not None
    assert po.name == "29 inch"
    assert po.part_category_id == pc.id
    assert po.base_price == Decimal("50.99")
    assert po.is_in_stock is True
    assert po.part_category.name == "Wheels"
    assert pc.part_options[0].name == "29 inch"

def test_cascade_delete_product_type(db_session: Session):
    """Test that deleting a ProductType cascades to PartCategory and PartOption."""
    # Setup
    pt = ProductType(name="Cascade Bike")
    pc = PartCategory(name="Drivetrain", product_type=pt)
    po = PartOption(name="10-speed", part_category=pc, base_price=100)
    db_session.add_all([pt, pc, po])
    db_session.commit()
    pt_id = pt.id
    pc_id = pc.id
    po_id = po.id

    # Ensure they exist
    assert db_session.get(ProductType, pt_id) is not None
    assert db_session.get(PartCategory, pc_id) is not None
    assert db_session.get(PartOption, po_id) is not None

    # Delete ProductType
    db_session.delete(pt)
    db_session.commit()

    # Check cascade
    assert db_session.get(ProductType, pt_id) is None
    assert db_session.get(PartCategory, pc_id) is None
    assert db_session.get(PartOption, po_id) is None 
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

def test_database_connection(db_session: Session):
    """Test that a connection to the database can be established."""
    try:
        # Execute a simple query
        db_session.execute(text("SELECT 1"))
        assert True # If execute succeeds, connection is assumed successful
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}") 
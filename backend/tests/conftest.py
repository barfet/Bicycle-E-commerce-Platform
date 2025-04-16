import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# from sqlalchemy_utils import database_exists, create_database, drop_database
from app.main import app
from app.db.session import get_db
from app.config import settings
from app.db.base import Base

# Use a dedicated test database URL from environment variables
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
if not TEST_DATABASE_URL:
    # Optionally default to DATABASE_URL + '_test' or raise error
    print("WARNING: TEST_DATABASE_URL not set in .env, tests might not run correctly or use the wrong database.")
    # Fallback or raise error - For now, let it proceed, but it might fail later
    # raise ValueError("TEST_DATABASE_URL environment variable is not set!") 

# Engine for creating/dropping the test database
# Connect to the default postgres DB first to manage other DBs
# Ensure TEST_DATABASE_URL and DATABASE_URL are set in .env
if TEST_DATABASE_URL and settings.POSTGRES_DB:
    try:
        default_postgres_url = TEST_DATABASE_URL.replace(settings.POSTGRES_DB + "_test", "postgres")
        temp_engine = create_engine(default_postgres_url, isolation_level="AUTOCOMMIT")
    except Exception as e:
        print(f"Error creating temp engine for DB management: {e}")
        temp_engine = None
else:
    temp_engine = None
    print("Skipping test database management setup due to missing URLs in config.")

# Engine for test sessions connected to the actual test DB
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Creates the test database and tables before tests run and drops them after."""
    if not engine or not temp_engine:
        print("Skipping test DB setup/teardown as engines are not configured.")
        yield # Allow tests to run, they might fail later
        return

    db_url = engine.url
    test_db_name = db_url.database

    # Connect with the temporary engine to create the database
    with temp_engine.connect() as conn:
        # Check if the database exists
        existing_dbs_query = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{test_db_name}'"))
        db_exists = existing_dbs_query.scalar() == 1

        if db_exists:
            print(f"Dropping existing test database: {test_db_name}")
            # Terminate connections before dropping
            conn.execute(text(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{test_db_name}';"))
            conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))

        print(f"Creating test database: {test_db_name}")
        conn.execute(text(f"CREATE DATABASE {test_db_name}"))

    # Now connect to the test database to create tables
    Base.metadata.create_all(bind=engine)
    yield

    # Teardown: Drop the test database
    print(f"Dropping test database: {test_db_name}")
    # Connect with the temporary engine again to drop
    with temp_engine.connect() as conn:
        # Terminate connections before dropping
        conn.execute(text(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{test_db_name}';"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
    temp_engine.dispose()
    engine.dispose()

@pytest.fixture(scope="function")
def db_session() -> Generator:
    """Provides a clean database session for each test function."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Provides a TestClient instance for API testing, overriding the DB dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    del app.dependency_overrides[get_db] # Clean up override 
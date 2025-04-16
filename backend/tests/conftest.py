import pytest
import pytest_asyncio # Import pytest-asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport # Import AsyncClient and ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
# Import async components
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy_utils import database_exists, create_database, drop_database
from app.main import app
from app.db.session import get_db # Now provides async session
from app.config import settings
from app.db.base import Base
from app.models import AdminUser, ProductType # Import ProductType
from app.schemas import ProductTypeCreate # Import ProductTypeCreate
from app.crud import create_product_type # Import async create_product_type
from app.core.security import hash_password

# Use a dedicated test database URL from environment variables
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
# Adjust URL prefix for asyncpg if needed
if TEST_DATABASE_URL and not TEST_DATABASE_URL.startswith("postgresql+asyncpg"):
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

if not TEST_DATABASE_URL:
    # Optionally default to DATABASE_URL + '_test' or raise error
    print("WARNING: TEST_DATABASE_URL not set in .env, tests might not run correctly or use the wrong database.")
    # Fallback or raise error - For now, let it proceed, but it might fail later
    # raise ValueError("TEST_DATABASE_URL environment variable is not set!")

# Engine for creating/dropping the test database (still synchronous is fine for setup/teardown)
# Connect to the default postgres DB first to manage other DBs
# Ensure TEST_DATABASE_URL and DATABASE_URL are set in .env
if settings.TEST_DATABASE_URL and settings.POSTGRES_DB: # Use original URL for sync engine
    try:
        original_test_db_url = settings.TEST_DATABASE_URL
        default_postgres_url = original_test_db_url.replace(settings.POSTGRES_DB + "_test", "postgres")
        temp_engine = create_engine(default_postgres_url, isolation_level="AUTOCOMMIT")
    except Exception as e:
        print(f"Error creating temp engine for DB management: {e}")
        temp_engine = None
else:
    temp_engine = None
    print("Skipping test database management setup due to missing URLs in config.")

# Synchronous engine needed only for Base.metadata.create_all
# This might cause issues if models rely on async-specific features not in sync engine
# Consider async alternative if problems arise
if settings.TEST_DATABASE_URL:
    sync_engine_for_metadata = create_engine(settings.TEST_DATABASE_URL) # Use original sync URL
else:
    sync_engine_for_metadata = None

# Async engine and sessionmaker for async tests
async_engine = create_async_engine(TEST_DATABASE_URL, echo=False) # Use adjusted async URL
AsyncTestingSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Creates the test database and tables before tests run and drops them after."""
    if not sync_engine_for_metadata or not temp_engine:
        print("Skipping test DB setup/teardown as engines are not configured.")
        yield # Allow tests to run, they might fail later
        return

    db_url = sync_engine_for_metadata.url
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

    # Now connect to the test database to create tables using the sync engine
    Base.metadata.create_all(bind=sync_engine_for_metadata)
    yield

    # Teardown: Drop the test database
    print(f"Dropping test database: {test_db_name}")
    # Connect with the temporary engine again to drop
    with temp_engine.connect() as conn:
        # Terminate connections before dropping
        conn.execute(text(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{test_db_name}';"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
    temp_engine.dispose()
    if sync_engine_for_metadata: sync_engine_for_metadata.dispose()
    # No dispose for async engine needed here?

# Async db fixture
@pytest_asyncio.fixture(scope="function") # Use pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Provides an async database session for each test function, rolling back changes within a nested transaction."""
    async with AsyncTestingSessionLocal() as session:
        # Begin a nested transaction for test isolation
        await session.begin_nested()
        yield session
        # Rollback the nested transaction after the test
        await session.rollback()
        # Close is handled by context manager

# Fixture for a test ProductType
@pytest_asyncio.fixture(scope="function")
async def test_product_type(db: AsyncSession) -> ProductType:
    """Fixture to create a test product type for dependency."""
    product_type_in = ProductTypeCreate(name="Test Bicycle Type")
    product_type = await create_product_type(db=db, product_type_in=product_type_in)
    return product_type

# Client fixture providing AsyncClient and overriding get_db
@pytest_asyncio.fixture(scope="function") # Use pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provides an AsyncClient instance for API testing, overriding the async DB dependency."""
    async def override_get_db_async() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncTestingSessionLocal() as session:
            # await session.begin()
            yield session
            # await session.rollback() # Rollback handled by db fixture if used directly

    app.dependency_overrides[get_db] = override_get_db_async
    # Correctly instantiate AsyncClient for FastAPI app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    del app.dependency_overrides[get_db] # Clean up override

# Test admin user fixture (now async)
@pytest_asyncio.fixture(scope="function") # Use pytest_asyncio.fixture
async def test_admin_user(db: AsyncSession) -> AdminUser:
    """Fixture to create a test admin user in the database for each test (async)."""
    username = "testfixtureadmin"
    password = "fixturepassword"
    hashed = hash_password(password)
    user = AdminUser(username=username, password_hash=hashed)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    # Store raw password for login tests
    user.raw_password = password
    return user

# Admin user headers fixture (now async)
@pytest_asyncio.fixture(scope="function") # Use pytest_asyncio.fixture
async def admin_user_headers(client: AsyncClient, test_admin_user: AdminUser) -> dict[str, str]:
    """Fixture to get authentication headers for the test admin user (async)."""
    # test_admin_user is already an awaitable fixture result, no need to await here
    # However, if the fixture *itself* was async, we might need `await test_admin_user` if not injected directly
    login_data = {
        "username": test_admin_user.username,
        "password": test_admin_user.raw_password, # Use the raw password stored earlier
    }
    # Use await with AsyncClient and correct URL, send as JSON
    response = await client.post("/api/v1/admin/login", json=login_data)
    assert response.status_code == 200, f"Failed to log in test admin user: {response.text}"
    tokens = response.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers 
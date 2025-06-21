import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app import app
from src.infrastructure.database import Base, get_db_session

# --- Test Database Setup ---
# Use an in-memory SQLite database for testing.
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# --- Fixture to Override Database Dependency ---
async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency override to provide a test database session.
    Each test will get a new session, and changes will be rolled back.
    """
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


# Apply the override to the FastAPI app.
app.dependency_overrides[get_db_session] = override_get_db_session


# --- Pytest Fixtures ---
@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the session.
    This is required for session-scoped async fixtures.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    """
    Initializes the test database before any tests run.
    The `autouse=True` ensures this fixture is used for all tests.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Teardown is handled by the in-memory nature of the database.


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an HTTP client for making requests to the test API.
    """
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c 
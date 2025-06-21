import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import settings

# Use the database URL from the central settings
engine = create_async_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)
Base = declarative_base()


async def get_db_session() -> AsyncSession:
    """Dependency to get a database session"""
    async with SessionLocal() as session:
        yield session


async def init_db():
    """Initialize the database and create tables"""
    # Ensure the directory for the database exists
    if settings.DATABASE_URL.startswith("sqlite"):
        db_path = settings.DATABASE_URL.split("///")[-1]
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    async with engine.begin() as conn:
        # This will create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close the database connection engine"""
    await engine.dispose() 
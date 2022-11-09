from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession)
Base = declarative_base()

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
test_async_session = sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession)

import typing as tp

import faker
import pytest_asyncio
from sqlalchemy import pool
from sqlalchemy.ext import asyncio as async_sql

from backend import config

settings = config.get_settings()

async_engine = async_sql.create_async_engine(settings.db_url, poolclass=pool.NullPool)
async_local_session = async_sql.async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=async_engine)

fake = faker.Faker()


@pytest_asyncio.fixture
async def db() -> tp.AsyncGenerator[async_sql.AsyncSession, None]:
    session = async_local_session()
    yield session
    await session.close()

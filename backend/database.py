import datetime as dt
import typing

import fastapi
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy import pool
from sqlalchemy import types
from sqlalchemy.ext import asyncio as sql_async

from backend import config

settings = config.get_settings()

DATABASE_URL = settings.db_url
engine = sql_async.create_async_engine(DATABASE_URL, poolclass=pool.NullPool)
async_session_maker = sql_async.async_sessionmaker(engine)


async def get_session():
    async_session = async_session_maker
    async with async_session() as session:
        yield session
    await session.close()

SessionDep = typing.Annotated[sql_async.AsyncSession, fastapi.Depends(get_session)]


class Base(sql_async.AsyncAttrs, orm.DeclarativeBase):
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sqlalchemy.func.now())
    updated_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now(), type_=types.TIMESTAMP(timezone=True))

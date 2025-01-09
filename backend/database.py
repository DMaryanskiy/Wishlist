import datetime as dt
import typing

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as sql_async

DATABASE_URL = 'postgresql+asyncpg://localhost/wishlist'
engine = sql_async.create_async_engine(DATABASE_URL)
async_session_maker = sql_async.async_sessionmaker(engine)


def get_database() -> typing.Generator:
    db = async_session_maker()
    try:
        yield db
    finally:
        db.close()


class Base(sql_async.AsyncAttrs, orm.DeclarativeBase):
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sqlalchemy.func.now())
    updated_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())

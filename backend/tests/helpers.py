from sqlalchemy.ext import asyncio as async_sql

from backend.users import models
from backend.users import auth
from backend.tests import conftest


async def create_user(db: async_sql.AsyncSession) -> models.Users:
    _user = models.Users(
        name=conftest.fake.name(),
        email=conftest.fake.email(),
        hashed_password=auth.get_password_hash(conftest.fake.password()),
    )

    db.add(_user)
    await db.commit()
    await db.refresh(_user, ['updated_at'])

    return _user


async def delete_fake_user(db: async_sql.AsyncSession, email: str) -> None:
    await models.user_crud.db_delete(db, allow_multiple=False, email=email)

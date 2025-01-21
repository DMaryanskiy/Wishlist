from sqlalchemy.ext import asyncio as async_sql

from backend.categories import models as categories_models
from backend.subscriptions import models as subscr_models
from backend.users import models as user_models
from backend.wishes import models as wishes_models
from backend.users import auth
from backend.tests import conftest


async def create_user(db: async_sql.AsyncSession) -> user_models.Users:
    _user = user_models.Users(
        name=conftest.fake.name(),
        email=conftest.fake.email(),
        hashed_password=auth.get_password_hash(conftest.fake.password()),
    )

    db.add(_user)
    await db.commit()
    await db.refresh(_user, ['updated_at'])

    return _user


async def create_subscription(db: async_sql.AsyncSession) -> subscr_models.Subscriptions:
    _user_1 = await create_user(db)
    _user_2 = await create_user(db)

    _subscription = subscr_models.Subscriptions(
        subscriber=_user_1.id,
        subscription=_user_2.id,
    )

    db.add(_subscription)
    await db.commit()
    await db.refresh(_subscription, ['updated_at'])

    return _subscription


async def create_wish(db: async_sql.AsyncSession, user_id: int) -> wishes_models.Wishes:
    _wish = wishes_models.Wishes(
        name=conftest.fake.name(),
        description='',
        link='',
        image='',
        user=user_id,
    )

    db.add(_wish)
    await db.commit()
    await db.refresh(_wish, ['updated_at'])

    return _wish


async def create_user_category(db: async_sql.AsyncSession, user_id: int) -> categories_models.UserCategories:
    _category = categories_models.UserCategories(
        name=conftest.fake.name(),
        user=user_id,
    )

    db.add(_category)
    await db.commit()
    await db.refresh(_category, ['updated_at'])

    return _category


async def create_wish_category(
    db: async_sql.AsyncSession,
    category_id: int,
    wish_id: int,
) -> categories_models.WishCategories:
    _category = categories_models.WishCategories(
        category_id=category_id,
        wish=wish_id,
    )

    db.add(_category)
    await db.commit()
    await db.refresh(_category, ['updated_at'])

    return _category


async def delete_fake_user(db: async_sql.AsyncSession, email: str) -> None:
    await user_models.user_crud.db_delete(db, allow_multiple=False, email=email)


async def delete_fake_subscription(db: async_sql.AsyncSession, subscription: subscr_models.Subscriptions) -> None:
    _user = await user_models.user_crud.get(db, id=subscription.subscriber, is_deleted=False)
    await delete_fake_user(db, _user['email'])

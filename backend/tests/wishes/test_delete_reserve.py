import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth


@pytest.mark.asyncio
async def test_ok(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)

    wish_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, wish_creator.id)

    _ = await helpers.reserve_wish(db, user.id, wish.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            f'/api/v1/wishes/{wish.id}/reserve',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    assert response.status_code == 204

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_not_own_forbidden(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)

    wish_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, wish_creator.id)

    _ = await helpers.reserve_wish(db, wish_creator.id, wish.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            f'/api/v1/wishes/{wish.id}/reserve',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Желание не зарезервировано или зарезервировано не Вами!'}

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_not_reserved(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)

    wish_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, wish_creator.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            f'/api/v1/wishes/{wish.id}/reserve',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Желание не зарезервировано или зарезервировано не Вами!'}

    await helpers.delete_fake_user(db, user.email)

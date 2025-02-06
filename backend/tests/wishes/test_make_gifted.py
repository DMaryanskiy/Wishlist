import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth


@pytest.mark.asyncio
async def test_ok_post(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            f'/api/v1/wishes/{wish.id}/gifted',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    assert response.status_code == 200
    data = response.json()

    assert data == {'success': True}

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_ok_delete(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            f'/api/v1/wishes/{wish.id}/gifted',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            f'/api/v1/wishes/{wish.id}/gifted',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    assert response.status_code == 200
    data = response.json()

    assert data == {'success': True}

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_forbidden(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    
    wish_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, wish_creator.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            f'/api/v1/wishes/{wish.id}/gifted',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    assert response.status_code == 403
    data = response.json()

    assert data == {'detail': 'Изменение не своего желания или категории запрещено!'}

    await helpers.delete_fake_user(db, user.email)
    await helpers.delete_fake_user(db, wish_creator.email)

import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth


@pytest.mark.asyncio
async def test_ok(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/categories/create',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'name': 'New category',
            },
        )
    
    assert response.status_code == 201
    data = response.json()

    assert data == {
        'user': user.email,
        'name': 'New category',
    }

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_category_exists(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    category = await helpers.create_user_category(db, user.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/categories/create',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'name': category.name,
            },
        )
    
    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Категория уже существует!'}

    await helpers.delete_fake_user(db, user.email)

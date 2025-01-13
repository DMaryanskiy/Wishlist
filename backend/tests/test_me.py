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
        response = await ac.get('/api/v1/auth/me', headers={
            'Authorization': f'Bearer {refresh_token}',
        })
    
    assert response.status_code == 200
    data = response.json()

    assert data == {
        'email': user.email,
        'name': user.name,
    }

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_not_authorized(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.get('/api/v1/auth/me')
    
    assert response.status_code == 401
    data = response.json()

    assert data == {'detail': 'Not authenticated'}

    await helpers.delete_fake_user(db, user.email)

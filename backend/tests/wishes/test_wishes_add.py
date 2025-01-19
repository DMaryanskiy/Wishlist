import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth
from backend.users import models


@pytest.mark.asyncio
async def test_ok(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/wishes/create',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'name': 'New wish',
            }
        )
    
    assert response.status_code == 201
    data = response.json()

    assert data == {
        'user': user.name,
        'name': 'New wish',
    }

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_bad(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/wishes/create',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'description': 'New wish',
            }
        )
    
    assert response.status_code == 422
    await helpers.delete_fake_user(db, user.email)

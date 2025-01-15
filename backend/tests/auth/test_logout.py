import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth


@pytest.mark.asyncio
async def test_ok_logout(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
        '/api/v1/auth/logout',
        cookies={
            'refresh_token': refresh_token,
        },
        headers={
            'Authorization': f'Bearer {refresh_token}',
        },
    )
    
    assert response.status_code == 200
    data = response.json()

    assert data == {'message': 'Токен был успешно удален!'}

    cookies = response.cookies
    assert not cookies.keys()

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_invalid_logout(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user.name}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
        '/api/v1/auth/logout',
        cookies={
            'refresh_token': refresh_token,
        },
        headers={
            'Authorization': f'Bearer {refresh_token}',
        },
    )
    
    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Пользователь был удален!'}

    await helpers.delete_fake_user(db, user.email)

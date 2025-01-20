import httpx
import pytest
from jose import jwt
from sqlalchemy.ext import asyncio as async_sql

from backend import config
from backend import main
from backend.tests import conftest
from backend.tests import helpers
from backend.users import auth

settings = config.get_settings()


@pytest.mark.asyncio
async def test_ok_edit(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    email = conftest.fake.email()
    name = conftest.fake.name()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.put(
            '/api/v1/auth/me/edit',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'email': email,
                'name': name,
                'password': conftest.fake.password(),
            },
        )
    
    assert response.status_code == 201
    data = response.json()

    assert data == {
        'email': email,
        'name': name,
    }

    cookies = response.cookies
    new_refresh = cookies.pop('refresh_token')

    assert refresh_token != new_refresh

    payload = jwt.decode(new_refresh, settings.secret_key, [settings.algorithm])
    token_email: str | None = payload.get('sub')

    assert token_email == email

    await helpers.delete_fake_user(db, email)


@pytest.mark.asyncio
async def test_edit_already_exists(db: async_sql.AsyncSession):
    existing_user = await helpers.create_user(db)

    user = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.put(
            '/api/v1/auth/me/edit',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'email': existing_user.email,
            },
        )
    
    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Пользователь уже существует!'}

    await helpers.delete_fake_user(db, user.email)
    await helpers.delete_fake_user(db, existing_user.email)

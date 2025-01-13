import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import conftest
from backend.tests import helpers
from backend.users import auth


@pytest.mark.asyncio
async def test_ok_login():
    # I need to remember raw password
    email = conftest.fake.email()
    password = conftest.fake.password()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/register', json={
            'email': email,
            'name': conftest.fake.name(),
            'password': password,
            'password_check': password,
        })

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/login', data={
            'username': email,
            'password': password,
        })

    assert response.status_code == 200
    cookies = response.cookies

    assert 'refresh_token' in cookies.keys()


@pytest.mark.asyncio
async def test_wrong_password(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/login', data={
            'username': user.email,
            'password': 'wrong_password',
        })
    
    assert response.status_code == 401
    data = response.json()

    assert data == {'detail': 'Неверная почта или пароль!'}


@pytest.mark.asyncio
async def test_ok_refresh(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/refresh', cookies={
            'refresh_token': refresh_token,
        })
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_no_refresh_token():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/refresh')
    
    assert response.status_code == 401
    data = response.json()

    assert data == {'detail': 'Отсутствует токен обновления или он некорректный!'}


@pytest.mark.asyncio
async def test_wrong_refresh_token():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/refresh', cookies={
            'refresh_token': 'refresh_token',
        })
    
    assert response.status_code == 401
    data = response.json()

    assert data == {'detail': 'Отсутствует токен обновления или он некорректный!'}

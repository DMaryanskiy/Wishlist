import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import conftest
from backend.tests import helpers


@pytest.mark.asyncio
async def test_ok():
    password = conftest.fake.password()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/register', json={
            'email': conftest.fake.email(),
            'name': conftest.fake.name(),
            'password': password,
            'password_check': password,
        })

    assert response.status_code == 201
    data = response.json()

    assert data['status'] == 'success'


@pytest.mark.asyncio
async def test_password_different():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/register', json={
            'email': conftest.fake.email(),
            'name': conftest.fake.name(),
            'password': conftest.fake.password(),
            'password_check': conftest.fake.password(),
        })

    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Пароли не совпадают!'}


@pytest.mark.asyncio
async def test_user_already_exists(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    password = conftest.fake.password()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post('/api/v1/auth/register', json={
            'email': user.email,
            'name': conftest.fake.name(),
            'password': password,
            'password_check': password,
        })

    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Пользователь уже существует!'}

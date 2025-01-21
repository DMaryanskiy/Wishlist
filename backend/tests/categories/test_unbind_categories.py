import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth


@pytest.mark.asyncio
async def test_ok(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user.id)
    category = await helpers.create_user_category(db, user.id)
    _ = await helpers.create_wish_category(db, category.category_id, wish.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            params={
                'category_id': category.category_id,
                'wish_id': wish.id,
            },
        )
    
    assert response.status_code == 204

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_bind_does_not_exist(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user.id)
    category = await helpers.create_user_category(db, user.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            params={
                'category_id': category.category_id,
                'wish_id': wish.id,
            },
        )
    
    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Желание уже отвязано от этой категории!'}

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_forbidden_category(db: async_sql.AsyncSession):
    user_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user_creator.id)
    category = await helpers.create_user_category(db, user_creator.id)
    _ = await helpers.create_wish_category(db, category.category_id, wish.id)

    user_editor = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user_editor.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            params={
                'category_id': category.category_id,
                'wish_id': wish.id,
            },
        )
    
    assert response.status_code == 403
    data = response.json()

    assert data == {'detail': 'Изменение не своего желания или категории запрещено!'}


@pytest.mark.asyncio
async def test_forbidden_wish(db: async_sql.AsyncSession):
    user_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user_creator.id)

    user_editor = await helpers.create_user(db)
    category = await helpers.create_user_category(db, user_editor.id)

    _ = await helpers.create_wish_category(db, category.category_id, wish.id)

    refresh_token = await auth.create_tokens({'sub': user_editor.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            params={
                'category_id': category.category_id,
                'wish_id': wish.id,
            },
        )
    
    assert response.status_code == 403
    data = response.json()

    assert data == {'detail': 'Изменение не своего желания или категории запрещено!'}


@pytest.mark.asyncio
async def test_bad_query(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user.id)
    category = await helpers.create_user_category(db, user.id)
    _ = await helpers.create_wish_category(db, category.category_id, wish.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )
    
    assert response.status_code == 400
    data = response.json()

    assert data == {'detail': 'Отсутствуют некоторые квери параметры!'}

    await helpers.delete_fake_user(db, user.email)

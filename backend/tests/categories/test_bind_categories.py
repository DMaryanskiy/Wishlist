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

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'category_id': category.category_id,
                'wish': wish.id,
            },
        )
    
    assert response.status_code == 201
    data = response.json()

    assert data == {
        'category_id': category.category_id,
        'wish': wish.id,
    }

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_bind_exists(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user.id)
    category = await helpers.create_user_category(db, user.id)
    _ = await helpers.create_wish_category(db, category.category_id, wish.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'category_id': category.category_id,
                'wish': wish.id,
            },
        )
    
    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Желание уже привязано к этой категории!'}

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_forbidden_category(db: async_sql.AsyncSession):
    user_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user_creator.id)
    category = await helpers.create_user_category(db, user_creator.id)

    user_editor = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user_editor.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'category_id': category.category_id,
                'wish': wish.id,
            },
        )
    
    assert response.status_code == 403
    data = response.json()

    assert data == {'detail': 'Изменение не своего желания или категории запрещено!'}

    await helpers.delete_fake_user(db, user_creator.email)
    await helpers.delete_fake_user(db, user_editor.email)


@pytest.mark.asyncio
async def test_forbidden_wish(db: async_sql.AsyncSession):
    user_creator = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user_creator.id)

    user_editor = await helpers.create_user(db)
    category = await helpers.create_user_category(db, user_editor.id)
    refresh_token = await auth.create_tokens({'sub': user_editor.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.post(
            '/api/v1/categories/bind',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
            json={
                'category_id': category.category_id,
                'wish': wish.id,
            },
        )
    
    assert response.status_code == 403
    data = response.json()

    assert data == {'detail': 'Изменение не своего желания или категории запрещено!'}

    await helpers.delete_fake_user(db, user_creator.email)
    await helpers.delete_fake_user(db, user_editor.email)

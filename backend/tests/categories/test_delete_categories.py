import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth


@pytest.mark.asyncio
async def test_ok(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    category = await helpers.create_user_category(db, user.id)

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            f'/api/v1/categories/{category.category_id}',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )
    
    assert response.status_code == 204

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_forbidden(db: async_sql.AsyncSession):
    user_creator = await helpers.create_user(db)
    category = await helpers.create_user_category(db, user_creator.id)

    user_editor = await helpers.create_user(db)
    refresh_token = await auth.create_tokens({'sub': user_editor.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(
            f'/api/v1/categories/{category.category_id}',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )
    
    assert response.status_code == 403
    data = response.json()

    assert data == {'detail': 'Изменение не своего желания или категории запрещено!'}

import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth
from backend.users import models


@pytest.mark.asyncio
async def test_ok(db: async_sql.AsyncSession):
    subscription = await helpers.create_subscription(db)

    subscriber = await models.user_crud.get(db, id=subscription.subscriber, is_deleted=False)

    refresh_token = await auth.create_tokens({'sub': subscriber['email']}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(f'/api/v1/subscribe/{subscription.subscription}', headers={
            'Authorization': f'Bearer {refresh_token}',
        })
    
    assert response.status_code == 204

    await helpers.delete_fake_subscription(db, subscription)


@pytest.mark.asyncio
async def test_subscription_does_not_exist(db: async_sql.AsyncSession):
    subscriber = await helpers.create_user(db)
    subscription = await helpers.create_user(db)

    refresh_token = await auth.create_tokens({'sub': subscriber.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.delete(f'/api/v1/subscribe/{subscription.id}', headers={
            'Authorization': f'Bearer {refresh_token}',
        })

    assert response.status_code == 409
    data = response.json()

    assert data == {'detail': 'Подписки не существует!'}

    await helpers.delete_fake_user(db, subscriber.email)
    await helpers.delete_fake_user(db, subscription.email)

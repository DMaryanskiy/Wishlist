import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import models


@pytest.mark.asyncio
async def test_ok_subscribers(db: async_sql.AsyncSession):
    subscription_obj = await helpers.create_subscription(db)

    subscriber = await models.user_crud.get(db, id=subscription_obj.subscriber, is_deleted=False)
    subscription = await models.user_crud.get(db, id=subscription_obj.subscription, is_deleted=False)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.get(f'/api/v1/subscribe/{subscription['id']}/get/subscribers')
    
    assert response.status_code == 200
    data = response.json()

    assert data == [
        {
            'email': subscriber['email'],
            'name': subscriber['name'],
        },
    ]

    await helpers.delete_fake_subscription(db, subscription_obj)


@pytest.mark.asyncio
async def test_ok_subscriptions(db: async_sql.AsyncSession):
    subscription_obj = await helpers.create_subscription(db)

    subscriber = await models.user_crud.get(db, id=subscription_obj.subscriber, is_deleted=False)
    subscription = await models.user_crud.get(db, id=subscription_obj.subscription, is_deleted=False)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.get(f'/api/v1/subscribe/{subscriber['id']}/get/subscriptions')
    
    assert response.status_code == 200
    data = response.json()

    assert data == [
        {
            'email': subscription['email'],
            'name': subscription['name'],
        },
    ]

    await helpers.delete_fake_subscription(db, subscription_obj)

import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.users import auth
from backend.wishes import schemas


@pytest.mark.asyncio
async def test_ok(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)

    wish_creator = await helpers.create_user(db)
    wishes = [
        await helpers.create_wish(db, wish_creator.id)
        for _ in range(5)
    ]

    _ = [
        await helpers.reserve_wish(db, user.id, wish.id)
        for wish in wishes
    ]

    refresh_token = await auth.create_tokens({'sub': user.email}, 'refresh')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.get(
            '/api/v1/wishes/get/reserved',
            headers={
                'Authorization': f'Bearer {refresh_token}',
            },
        )

    assert response.status_code == 200
    data = response.json()

    wish_json = [schemas.WishesBase.model_validate(wish.__dict__) for wish in wishes]
    assert data == [wish.model_dump() for wish in wish_json]

    await helpers.delete_fake_user(db, user.email)
    await helpers.delete_fake_user(db, wish_creator.email)

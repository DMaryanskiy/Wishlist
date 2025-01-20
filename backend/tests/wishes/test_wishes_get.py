import httpx
import pytest
from sqlalchemy.ext import asyncio as async_sql

from backend import main
from backend.tests import helpers
from backend.wishes import schemas


@pytest.mark.asyncio
async def test_ok_by_user(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wishes = [await helpers.create_wish(db, user.id) for _ in range(5)]

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.get(
            f'/api/v1/wishes/{user.id}',
        )
    
    assert response.status_code == 200
    data = response.json()

    wishes_response = [schemas.WishesBase(**wish.__dict__).model_dump() for wish in wishes]
    assert data == wishes_response

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_ok_by_subsrtring(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    wish = await helpers.create_wish(db, user.id)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.get(
            f'/api/v1/wishes/by_substring?substring={wish.name}',
        )
    
    assert response.status_code == 200
    data = response.json()

    assert data == [
        {
            'name': wish.name,
            'description': wish.description,
            'link': wish.link,
            'image': wish.image,
        },
    ]

    await helpers.delete_fake_user(db, user.email)


@pytest.mark.asyncio
async def test_ok_by_empty_subsrtring(db: async_sql.AsyncSession):
    user = await helpers.create_user(db)
    _ = await helpers.create_wish(db, user.id)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://localhost') as ac:
        response = await ac.get(
            f'/api/v1/wishes/by_substring',
        )
    
    assert response.status_code == 200
    data = response.json()

    assert data == []

    await helpers.delete_fake_user(db, user.email)

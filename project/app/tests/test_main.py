import asyncio

import pytest
from app.db.config import Base, test_async_session, test_engine
from app.tests.static_responses import fibonacci_13, fibonacci_list_5
from httpx import AsyncClient

from ..main import app, get_session


async def override_get_session():
    try:
        db = test_async_session()
        yield db
    finally:
        await db.close()


async def init_models():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

app.dependency_overrides[get_session] = override_get_session


@pytest.mark.asyncio
async def test_fibonacci():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/fibonacci/", params={"number": 13})
        assert response.status_code == 200
        assert response.json() == fibonacci_13

        response = await async_client.get("/fibonacci/", params={"number": -10})
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_fibonacci_list():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        search_number_object = {"number": 5}
        deleted_number_object = {"number": 2, "fibonacci_number": 1}
        response = await async_client.get("/fibonacci/list", params=search_number_object)
        assert response.status_code == 200
        assert response.json() == fibonacci_list_5

        response = await async_client.post(
            "/fibonacci/add_to_blacklist", params={"number": deleted_number_object["number"]}
        )
        assert response.status_code == 200

        response = await async_client.get("/fibonacci/list", params=search_number_object)
        assert response.status_code == 200
        assert deleted_number_object not in response.json()['items']

        response = await async_client.get("/fibonacci/list", params={"number": 0})
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_to_blacklist():
    add_number_object = {"number": 10}
    add_number_object2 = {"number": 100}
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post(
            "/fibonacci/add_to_blacklist",
            params=add_number_object
        )
        assert response.status_code == 200

        response = await async_client.post(
            "/fibonacci/add_to_blacklist",
            params=add_number_object2
        )
        assert response.status_code == 200

        response = await async_client.get("/fibonacci/blacklist")
        assert response.status_code == 200
        assert all(value in response.json()
                   for value in [add_number_object, add_number_object2])


@pytest.mark.asyncio
async def test_delete_from_blacklist():
    add_delete_number_object = {"number": 100}
    async with AsyncClient(app=app, base_url="http://test") as async_client:

        response = await async_client.post(
            "/fibonacci/add_to_blacklist", params=add_delete_number_object
        )
        assert response.status_code == 200

        response = await async_client.delete(
            "/fibonacci/delete_from_blacklist", params=add_delete_number_object
        )
        assert response.status_code == 200

        response = await async_client.get("/fibonacci/blacklist")
        assert response.status_code == 200
        assert add_delete_number_object not in response.json()

import random
import string
import sys

import pytest
from sqlalchemy import text

sys.path.append("..")
sys.path.append(".")

from fastapi.testclient import TestClient
from src.__main__ import app
import asyncio




@pytest.fixture(scope="session")
def test_app():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def login_headers(test_app: TestClient):
    response = test_app.post("/login/register",
            json={"email":  f"testtest@ya.ru",
                "password": "nfhreb123ui"}, )
    assert response.status_code == 200

    test_app.post("/login/register",
            json={"email":  "test@test.org",
                "password": "nfhreb123ui"}, )

    return {"Authorization": f"Bearer {response.json().get('jwtToken')}"}

@pytest.fixture(scope="session", autouse=True)
def truncate_db():
    async def truncate():
        async with async_sessionmaker() as session:
            await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE projects RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE achievements RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE achievement_folder RESTART IDENTITY CASCADE"))
            await session.commit()

    import src.settings
    import sqlalchemy.ext.asyncio
    settings = src.settings.Settings()

    engine = sqlalchemy.ext.asyncio.create_async_engine(settings.DB_URL)
    async_sessionmaker = sqlalchemy.ext.asyncio.async_sessionmaker(
            bind=engine, expire_on_commit=False
    )

    asyncio.run(truncate())

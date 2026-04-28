import pytest
import httpx
from httpx import ASGITransport
from faker import Faker
from itertools import count
from app.main import app as fastapi_app, db
import app.main


@pytest.fixture(scope="function")
def faker_instance():
    """Фикстура для генерации реалистичных тестовых данных"""
    return Faker(locale="ru_RU")


@pytest.fixture(scope="function")
async def async_client():
    """
    Асинхронный HTTP-клиент с ASGITransport.
    Запросы идут напрямую в приложение, без запуска Uvicorn.
    """
    db.clear()
    app.main._id_seq = count(start=1)
    app.main.next_user_id = lambda: next(app.main._id_seq)
    
    transport = ASGITransport(app=fastapi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
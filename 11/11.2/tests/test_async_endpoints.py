import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestAsyncUserEndpoints:
    """Асинхронные тесты для CRUD-операций с пользователем"""

    async def test_create_user_success(self, async_client, faker_instance):
        """✅ Создание пользователя: 201 + валидация структуры ответа"""
        payload = {
            "username": faker_instance.user_name(),
            "age": faker_instance.random_int(min=19, max=80)
        }
        response = await async_client.post("/users", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == payload["username"]
        assert data["age"] == payload["age"]
        assert isinstance(data["id"], int)

    async def test_get_existing_user(self, async_client, faker_instance):
        """✅ Получение существующего пользователя: 200"""
        # Сначала создаём
        create_resp = await async_client.post("/users", json={
            "username": faker_instance.first_name(),
            "age": 25
        })
        user_id = create_resp.json()["id"]
        
        # Затем получаем
        response = await async_client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    async def test_get_non_existing_user(self, async_client):
        """❌ Получение несуществующего пользователя: 404"""
        response = await async_client.get("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    async def test_delete_existing_user(self, async_client, faker_instance):
        """✅ Удаление существующего пользователя: 204"""
        # Создаём пользователя
        create_resp = await async_client.post("/users", json={
            "username": faker_instance.last_name(),
            "age": 30
        })
        user_id = create_resp.json()["id"]
        
        # Удаляем
        response = await async_client.delete(f"/users/{user_id}")
        assert response.status_code == 204
        
        # Проверяем, что действительно удалён
        get_resp = await async_client.get(f"/users/{user_id}")
        assert get_resp.status_code == 404

    async def test_delete_non_existing_user(self, async_client):
        """❌ Удаление несуществующего пользователя: 404"""
        response = await async_client.delete("/users/12345")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    async def test_create_user_boundary_values(self, async_client, faker_instance):
        """🔍 Граничные значения: минимальный возраст (19) и максимальный (100)"""
        for age in [19, 100]:
            payload = {"username": faker_instance.user_name(), "age": age}
            response = await async_client.post("/users", json=payload)
            assert response.status_code == 201
            assert response.json()["age"] == age
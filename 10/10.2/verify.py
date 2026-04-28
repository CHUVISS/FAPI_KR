from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("🚀 Запуск проверки валидации и обработки ошибок...\n")

    # Валидный запрос
    valid_payload = {
        "username": "alex_dev",
        "age": 25,
        "email": "alex@example.com",
        "password": "superSecret123",
        "phone": "+79001234567"
    }
    r = client.post("/register", json=valid_payload)
    assert r.status_code == 201
    assert r.json()["status"] == "success"
    print("✅ POST /register (valid) → 201 OK")

    # Неверный age (должно быть > 18)
    r = client.post("/register", json={**valid_payload, "age": 16})
    assert r.status_code == 422
    print("✅ POST /register (age=16) → 422 Validation Error")

    # Неверный email
    r = client.post("/register", json={**valid_payload, "email": "not-an-email"})
    assert r.status_code == 422
    print("✅ POST /register (bad email) → 422 Validation Error")

    # Слишком короткий пароль
    r = client.post("/register", json={**valid_payload, "password": "123"})
    assert r.status_code == 422
    print("✅ POST /register (short password) → 422 Validation Error")

    # Проверка структуры ответа об ошибке
    error_resp = r.json()
    assert "status_code" in error_resp
    assert "message" in error_resp
    assert "details" in error_resp
    print(f"\n📋 Пример ответа ошибки:\n{error_resp}")

    print("\n🎉 Все тесты пройдены успешно!")

if __name__ == "__main__":
    run_tests()
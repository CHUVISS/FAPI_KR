from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("🚀 Запуск проверки кастомной обработки ошибок...\n")

    # Успешные сценарии
    r = client.get("/validate/10")
    assert r.status_code == 200
    print("/validate/10 → 200 OK")

    r = client.get("/resource/42")
    assert r.status_code == 200
    print("/resource/42 → 200 OK")

    #Проверка CustomExceptionA
    r = client.get("/validate/-5")
    assert r.status_code == 400
    data = r.json()
    assert data["status_code"] == 400
    assert data["message"] == "Ошибка проверки условия"
    print("/validate/-5 → 400 (CustomExceptionA)")
    print(f"   Ответ: {data}")

    #Проверка CustomExceptionB
    r = client.get("/resource/999")
    assert r.status_code == 404
    data = r.json()
    assert data["status_code"] == 404
    assert data["message"] == "Ресурс не найден"
    print("/resource/999 → 404 (CustomExceptionB)")
    print(f"   Ответ: {data}")

    print("\nВсе тесты пройдены успешно!")

if __name__ == "__main__":
    run_tests()
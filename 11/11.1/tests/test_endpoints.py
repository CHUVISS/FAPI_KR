class TestUserEndpoints:
    def test_create_user_success(self, client):
        payload = {"username": "alice", "age": 25}
        response = client.post("/users", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["username"] == "alice"
        assert data["age"] == 25

    def test_create_user_validation_error(self, client):
        # Отправляем payload без обязательного поля age
        response = client.post("/users", json={"username": "bob"})
        assert response.status_code == 422

    def test_get_existing_user(self, client):
        client.post("/users", json={"username": "charlie", "age": 30})
        response = client.get("/users/1")
        assert response.status_code == 200
        assert response.json()["username"] == "charlie"

    def test_get_non_existing_user(self, client):
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_existing_user(self, client):
        client.post("/users", json={"username": "dave", "age": 28})
        response = client.delete("/users/1")
        assert response.status_code == 204
        # Проверяем, что пользователь действительно удалён
        assert client.get("/users/1").status_code == 404

    def test_delete_non_existing_user(self, client):
        response = client.delete("/users/500")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
import pytest
from fastapi.testclient import TestClient

from app.main import app as fastapi_app, db
import app.main

@pytest.fixture
def client():
    db.clear()
    app.main.next_id = 1
    with TestClient(fastapi_app) as test_client:
        yield test_client
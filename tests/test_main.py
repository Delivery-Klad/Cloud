from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_files():
    response = client.get("/files/")
    assert response.status_code == 200

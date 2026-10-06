import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.get_json()
    assert "version" in data
    assert data["status"] == "ok"

def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"

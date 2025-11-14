import os
from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)

def test_health():
    r = c.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"

def test_echo_and_sum_when_key_present():
    api_key = os.getenv("API_KEY", "")
    if not api_key:
        # when no key is set in env, protected routes should 401 in CI
        r = c.post("/echo", json={"message": "hi", "count": 2})
        assert r.status_code == 401
        r = c.post("/sum", json={"numbers": [1, 2, 3]})
        assert r.status_code == 401
        return

    headers = {"x-api-key": api_key}
    r = c.post("/echo", json={"message": "hi", "count": 2}, headers=headers)
    assert r.status_code == 200
    assert r.json()["echo"] == "hi"

    r = c.post("/sum", json={"numbers": [1, 2, 3]}, headers=headers)
    assert r.status_code == 200
    assert r.json()["sum"] == 6

from fastapi.testclient import TestClient
from main import app, cosine

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_summarize_rejects_missing_text():
    response = client.post("/summarize", json={})
    assert response.status_code == 422

def test_cosine_identical_vectors_is_one():
    v = [1.0, 2.0, 3.0]
    assert cosine(v, v) > 0.999

def test_cosine_orthogonal_vectors_is_near_zero():
    assert abs(cosine([1.0, 0.0], [0.0, 1.0])) < 0.001
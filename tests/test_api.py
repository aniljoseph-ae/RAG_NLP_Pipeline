import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_process_endpoint():
    response = client.post("/process", json={
        "tasks": [
            {"text": "Test text", "task_type": "sentiment_analysis"}
        ]
    })
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "processing"
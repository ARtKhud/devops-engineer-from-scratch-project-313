from unittest.mock import Mock

from fastapi.testclient import TestClient

from src.server import app
from src.services.link_service import get_link_service

client = TestClient(app)


def test_create_link_success():
    mock_service = Mock()
    request_data = {
        "original_url": "https://google.com",
        "short_name": "google",
    }
    expected_response = {
        "id": 1,
        "original_url": "https://google.com",
        "short_name": "google",
        "short_url": "https://short.ly/google",
    }
    mock_service.create_link.return_value = expected_response
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.post("/api/links", json=request_data)
        assert response.status_code == 201
        assert response.json() == expected_response

    finally:
        app.dependency_overrides.clear()


def test_create_link_with_short_url():
    mock_service = Mock()
    request_data = {
        "original_url": "https://example.com",
        "short_name": "example",
    }
    mock_response = {
        "id": 2,
        "original_url": "https://example.com",
        "short_name": "example",
        "short_url": "https://short.ly/example",
    }
    mock_service.create_link.return_value = mock_response
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.post("/api/links", json=request_data)
        assert response.status_code == 201
        assert "short_url" in response.json()
        assert response.json()["short_url"] == "https://short.ly/example"
    finally:
        app.dependency_overrides.clear()


def test_create_link_returns_correct_structure():
    mock_service = Mock()
    request_data = {"original_url": "https://test.com", "short_name": "test"}
    mock_response = {
        "id": 3,
        "original_url": "https://test.com",
        "short_name": "test",
        "short_url": "https://short.ly/test",
    }

    mock_service.create_link.return_value = mock_response
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.post("/api/links", json=request_data)
        data = response.json()
        assert "id" in data
        assert "original_url" in data
        assert "short_name" in data
        assert "short_url" in data
        assert isinstance(data["id"], int)
        assert isinstance(data["original_url"], str)
        assert isinstance(data["short_name"], str)
        assert isinstance(data["short_url"], str)
    finally:
        app.dependency_overrides.clear()


def test_create_with_invalid_value():
    mock_service = Mock()
    request_data = {}
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.post("/api/links", json=request_data)
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()

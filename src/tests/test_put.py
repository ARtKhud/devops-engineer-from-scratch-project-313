from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from src.server import app
from src.services.link_service import get_link_service

client = TestClient(app)


# def test_create_link_success():
#     mock_service = Mock()
#     request_data = {
#         "original_url": "https://google.com",
#         "short_name": "google",
#     }
#     expected_response = {
#         "id": 1,
#         "original_url": "https://google.com",
#         "short_name": "google",
#         "short_url": "https://short.ly/google",
#     }
#     mock_service.create_link.return_value = expected_response
#     app.dependency_overrides[get_link_service] = lambda: mock_service
#     try:
#         response = client.post("/api/links", json=request_data)
#         assert response.status_code == 201
#         assert response.json() == expected_response

#     finally:
#         app.dependency_overrides.clear()


def test_update_link_success():
    link_id = 1
    mock_service = Mock()
    request_data = {
        "original_url": "https://updated-example.com",
        "short_name": "updated-example",
    }

    mock_updated_link = {
        "id": link_id,
        "original_url": "https://updated-example.com",
        "short_name": "updated-example",
        "short_url": "https://short.ly/updated-example",
    }
    mock_service.update_link.return_value = mock_updated_link
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.put(f"/api/links/{link_id}", json=request_data)
        assert response.status_code == 200
        assert response.json() == mock_updated_link
    finally:
        app.dependency_overrides.clear()


def test_update_link_partial_data():
    link_id = 1
    mock_service = Mock()
    partial_data = {"short_name": "only-name-updated"}

    mock_updated_link = {
        "id": link_id,
        "original_url": "https://original-example.com",
        "short_name": "only-name-updated",
        "short_url": "https://short.ly/only-name-updated",
    }

    mock_service.update_link.return_value = mock_updated_link
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.put(f"/api/links/{link_id}", json=partial_data)
        assert response.status_code == 200
        assert response.json()["short_name"] == "only-name-updated"
    finally:
        app.dependency_overrides.clear()


def test_update_link_different_ids():
    mock_service = Mock()
    test_cases = [
        (1, {"short_name": "test1"}),
        (42, {"original_url": "https://test42.com"}),
        (999, {"original_url": "https://test999.com", "short_name": "test999"}),
    ]

    for link_id, update_data in test_cases:
        app.dependency_overrides[get_link_service] = lambda: mock_service
        mock_response = {
            "id": link_id,
            "original_url": update_data.get("original_url", "https://original.com"),
            "short_name": update_data.get("short_name", "original"),
            "short_url": (
                f"https://short.ly/{update_data.get('short_name', 'original')}"
            ),
        }
        mock_service.update_link.return_value = mock_response
        try:
            response = client.put(f"/api/links/{link_id}", json=update_data)
            assert response.status_code == 200
        finally:
            app.dependency_overrides.clear()

from unittest.mock import Mock

from fastapi.testclient import TestClient

from src.server import app
from src.services.link_service import get_link_service

client = TestClient(app)


def test_get_links():
    mock_service = Mock()
    mock_links = [
        {
            "id": 1,
            "original_url": "https://example.com",
            "short_name": "example",
            "short_url": "https://short.ly/example",
        }
    ]
    mock_service.get_all_links.return_value = mock_links
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.get("/api/links")
        assert response.status_code == 200
        assert response.json() == mock_links
    finally:
        app.dependency_overrides.clear()


def test_get_link_by_id_success():
    link_id = 1
    mock_service = Mock()
    mock_link = {
        "id": link_id,
        "original_url": "https://example.com",
        "short_name": "example",
        "short_url": "https://short.ly/example",
    }
    mock_service.get_all_links.return_value = mock_link
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        mock_service.get_link_by_id.return_value = mock_link
        response = client.get(f"/api/links/{link_id}")

        assert response.status_code == 200
        assert response.json() == mock_link
    finally:
        app.dependency_overrides.clear()


def test_get_link_by_id_different_ids():
    test_cases = [
        (
            1,
            {
                "id": 1,
                "original_url": "https://test1.com",
                "short_name": "test1",
            },
        ),
        (
            42,
            {
                "id": 42,
                "original_url": "https://test42.com",
                "short_name": "test42",
            },
        ),
        (
            999,
            {
                "id": 999,
                "original_url": "https://test999.com",
                "short_name": "test999",
            },
        ),
    ]
    mock_service = Mock()
    for link_id, mock_link in test_cases:
        app.dependency_overrides[get_link_service] = lambda: mock_service
        mock_service.get_link_by_id.return_value = mock_link
        try:
            response = client.get(f"/api/links/{link_id}")
            assert response.status_code == 200
            assert response.json() == mock_link
        finally:
            app.dependency_overrides.clear()


def test_get_links_with_range_query():
    mock_service = Mock()
    mock_links = [{"id": i, "short_name": f"test{i}"} for i in range(5)]
    mock_service.get_all_links.return_value = mock_links
    mock_service.get_total.return_value = 100
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.get("/api/links?range=[5,9]")
        assert response.status_code == 200
        assert "Content-Range" in response.headers
        assert response.headers["Content-Range"] == "links 5-9/100"
    finally:
        app.dependency_overrides.clear()


def test_get_links_default_pagination():
    mock_service = Mock()
    mock_links = [{"id": i, "short_name": f"test{i}"} for i in range(10)]
    mock_service.get_all_links.return_value = mock_links
    mock_service.get_total.return_value = 30
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        response = client.get("/api/links")
        assert response.status_code == 200
        assert "Content-Range" not in response.headers
    finally:
        app.dependency_overrides.clear()

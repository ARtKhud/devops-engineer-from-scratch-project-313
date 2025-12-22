from unittest.mock import Mock

from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.server import app
from src.services import get_link_service

client = TestClient(app)


def test_delete_link_success_204():
    link_id = 1
    mock_service = Mock()
    mock_service.delete_link.return_value = None
    app.dependency_overrides[get_link_service] = lambda: mock_service

    try:
        response = client.delete(f"/api/links/{link_id}")
        assert response.status_code == 204
        assert response.content == b""
        mock_service.delete_link.assert_called_once_with(link_id)
    finally:
        app.dependency_overrides.clear()


def test_delete_link_not_found_404():
    link_id = 999
    mock_service = Mock()
    mock_service.delete_link.return_value = None
    app.dependency_overrides[get_link_service] = lambda: mock_service
    try:
        mock_service.delete_link.side_effect = HTTPException(
            status_code=404, detail="Link not found"
        )
        response = client.delete(f"/api/links/{link_id}")
        assert response.status_code == 404
        response_data = response.json()
        assert "detail" in response_data
        assert response_data["detail"] == "Link not found"
    finally:
        app.dependency_overrides.clear()


def test_delete_link_different_ids():
    test_cases = [
        (1, 204),
        (999, 404),
        (42, 204),
        (0, 404),
    ]
    mock_service = Mock()
    mock_service.delete_link.return_value = None
    for link_id, expected_status in test_cases:
        app.dependency_overrides[get_link_service] = lambda: mock_service
        try:
            if expected_status == 204:
                mock_service.delete_link.side_effect = HTTPException(
                    status_code=204, detail="No Content"
                )
            else:
                mock_service.delete_link.side_effect = HTTPException(
                    status_code=404, detail="Link not found"
                )
            response = client.delete(f"/api/links/{link_id}")
            assert response.status_code == expected_status
        finally:
            app.dependency_overrides.clear()

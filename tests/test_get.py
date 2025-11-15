from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_pong():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == 'pong'


def test_get_links():
    mock_links = [
        {
            "id": 1,
            "original_url": "https://example.com",
            "short_name": "example", 
            "short_url": "https://short.ly/example"
        }
    ]
    with patch('app.main.repo') as mock_repo:
        mock_repo.get_content.return_value = mock_links
        response = client.get("/api/links")
        assert response.status_code == 200
        assert response.json() == mock_links
        mock_repo.get_content.assert_called_once()


def test_get_link_by_id_success():
    link_id = 1
    mock_link = {
        "id": link_id,
        "original_url": "https://example.com",
        "short_name": "example",
        "short_url": "https://short.ly/example"
    }
    
    with patch('app.main.repo') as mock_repo:
        mock_repo.find.return_value = mock_link
        
        response = client.get(f"/api/links/{link_id}")
        
        assert response.status_code == 200
        assert response.json() == mock_link
        mock_repo.find.assert_called_once_with(link_id)


def test_get_link_by_id_different_ids():
    test_cases = [
        (1, {"id": 1, "original_url": "https://test1.com",
              "short_name": "test1"}),
        (42, {"id": 42, "original_url": "https://test42.com",
               "short_name": "test42"}),
        (999, {"id": 999, "original_url": "https://test999.com",
                "short_name": "test999"})
    ]
    
    for link_id, mock_link in test_cases:
        with patch('app.main.repo') as mock_repo:
            mock_repo.find.return_value = mock_link
            
            response = client.get(f"/api/links/{link_id}")
            
            assert response.status_code == 200
            assert response.json() == mock_link
            mock_repo.find.assert_called_once_with(link_id)
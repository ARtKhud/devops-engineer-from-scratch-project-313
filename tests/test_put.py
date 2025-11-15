from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_update_link_success():
    link_id = 1
    request_data = {
        "original_url": "https://updated-example.com",
        "short_name": "updated-example"
    }
    
    mock_updated_link = {
        "id": link_id,
        "original_url": "https://updated-example.com",
        "short_name": "updated-example",
        "short_url": "https://short.ly/updated-example"
    }
    
    with patch('app.main.repo') as mock_repo:
        mock_repo._update.return_value = mock_updated_link
        
        response = client.put(f"/api/links/{link_id}", json=request_data)
        
        assert response.status_code == 200
        assert response.json() == mock_updated_link
        mock_repo._update.assert_called_once_with(link_id, request_data)


def test_update_link_partial_data():
    link_id = 1
    partial_data = {
        "short_name": "only-name-updated"
    }
    
    mock_updated_link = {
        "id": link_id,
        "original_url": "https://original-example.com", 
        "short_name": "only-name-updated", 
        "short_url": "https://short.ly/only-name-updated"
    }
    
    with patch('app.main.repo') as mock_repo:
        mock_repo._update.return_value = mock_updated_link
        
        response = client.put(f"/api/links/{link_id}", json=partial_data)
        
        assert response.status_code == 200
        assert response.json()["short_name"] == "only-name-updated"
        mock_repo._update.assert_called_once_with(link_id, partial_data)


def test_update_link_different_ids():
    test_cases = [
        (1, {"short_name": "test1"}),
        (42, {"original_url": "https://test42.com"}),
        (999, {"original_url": "https://test999.com", "short_name": "test999"})
    ]
    
    for link_id, update_data in test_cases:
        with patch('app.main.repo') as mock_repo:
            mock_response = {
                "id": link_id,
                "original_url": update_data.get("original_url", "https://original.com"),
                "short_name": update_data.get("short_name", "original"),
                "short_url": (
                f"https://short.ly/{update_data.get('short_name', 'original')}"
                )
            }
            mock_repo._update.return_value = mock_response
            
            response = client.put(f"/api/links/{link_id}", json=update_data)
            
            assert response.status_code == 200
            mock_repo._update.assert_called_once_with(link_id, update_data)
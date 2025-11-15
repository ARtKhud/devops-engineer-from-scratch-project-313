from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_link_success():
    request_data = {
        "original_url": "https://google.com",
        "short_name": "google"
    }
    
    expected_response = {
        "id": 1,
        "original_url": "https://google.com",
        "short_name": "google",
        "short_url": "https://short.ly/google"
    }
    
    with patch('app.main.repo') as mock_repo:
        mock_repo._create.return_value = expected_response
        
        response = client.post("/api/links", json=request_data)
        
        assert response.status_code == 200
        assert response.json() == expected_response
        
        mock_repo._create.assert_called_once_with(request_data)


def test_create_link_with_short_url():
    request_data = {
        "original_url": "https://example.com",
        "short_name": "example"
    }
    
    mock_response = {
        "id": 2,
        "original_url": "https://example.com",
        "short_name": "example",
        "short_url": "https://short.ly/example"  
    }
    
    with patch('app.main.repo') as mock_repo:
        mock_repo._create.return_value = mock_response
        
        response = client.post("/api/links", json=request_data)
        
        assert response.status_code == 200
        assert "short_url" in response.json()
        assert response.json()["short_url"] == "https://short.ly/example"


def test_create_link_returns_correct_structure():
    request_data = {
        "original_url": "https://test.com",
        "short_name": "test"
    }
    
    mock_response = {
        "id": 3,
        "original_url": "https://test.com",
        "short_name": "test",
        "short_url": "https://short.ly/test"
    }
    
    with patch('app.main.repo') as mock_repo:
        mock_repo._create.return_value = mock_response
        
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
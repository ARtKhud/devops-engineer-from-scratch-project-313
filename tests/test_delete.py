from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_delete_link_success_204():
    link_id = 1
    
    with patch('app.main.repo') as mock_repo:
        mock_repo.delete.side_effect = HTTPException(status_code=204,
                                                      detail="No Content")
        
        response = client.delete(f"/api/links/{link_id}")
        
        assert response.status_code == 204
        
        assert response.content == b""
        assert mock_repo.delete.called
        mock_repo.delete.assert_called_once_with(link_id)


def test_delete_link_not_found_404():
    link_id = 999
    
    with patch('app.main.repo') as mock_repo:
        mock_repo.delete.side_effect = HTTPException(
            status_code=404, 
            detail="Link not found"
        )
        
        response = client.delete(f"/api/links/{link_id}")
        
        assert response.status_code == 404
        
        response_data = response.json()
        assert "detail" in response_data
        assert response_data["detail"] == "Link not found"
        
        mock_repo.delete.assert_called_once_with(link_id)


def test_delete_link_different_ids():
    test_cases = [
        (1, 204), 
        (999, 404), 
        (42, 204), 
        (0, 404), 
    ]
    
    for link_id, expected_status in test_cases:
        with patch('app.main.repo') as mock_repo:
            if expected_status == 204:
                mock_repo.delete.side_effect = HTTPException(status_code=204,
                    detail="No Content")
            else:
                mock_repo.delete.side_effect = HTTPException(status_code=404,
                    detail="Link not found")
            
            response = client.delete(f"/api/links/{link_id}")
            
            assert response.status_code == expected_status
            mock_repo.delete.assert_called_once_with(link_id)

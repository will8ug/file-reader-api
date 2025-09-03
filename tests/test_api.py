import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPI:
    def test_root_endpoint(self):
        """Test the root endpoint returns basic API information."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "File Reader API"
        assert data["version"] == "0.1.0"
        assert "prompt_templates" in data["endpoints"]
    
    def test_get_all_prompts(self):
        """Test getting all prompts without code parameter."""
        response = client.get("/api/prompt-templates")
        assert response.status_code == 200
        
        data = response.json()
        assert "prompts" in data
        assert len(data["prompts"]) > 0
        
        # Check that only metadata is returned (no content)
        first_prompt = data["prompts"][0]
        assert "name" in first_prompt
        assert "code" in first_prompt
        assert "scope" in first_prompt
        assert "params" in first_prompt
        assert "file" in first_prompt
        assert "content" not in first_prompt
    
    def test_get_prompt_by_code(self):
        """Test getting a specific prompt by code."""
        response = client.get("/api/prompt-templates?code=1")
        assert response.status_code == 200
        
        data = response.json()
        assert "prompt" in data
        
        prompt = data["prompt"]
        assert prompt["code"] == 1
        assert prompt["name"] == "hello"
        assert "content" in prompt
        assert "file" not in prompt
        assert "Hello, {name}! Welcome!" in prompt["content"]
    
    def test_get_prompt_by_invalid_code(self):
        """Test getting a prompt with invalid code returns 404."""
        response = client.get("/api/prompt-templates?code=999")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"

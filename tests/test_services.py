import pytest
from pathlib import Path
from app.services import PromptService
from app.models import PromptMetadata, PromptTemplate


class TestPromptService:
    @pytest.fixture
    def service(self):
        return PromptService()
    
    def test_get_all_prompts(self, service):
        """Test getting all prompts returns metadata without file content."""
        prompts = service.get_all_prompts()
        
        assert len(prompts) > 0
        assert all(isinstance(prompt, PromptMetadata) for prompt in prompts)
        
        # Check that the first prompt has the expected structure
        first_prompt = prompts[0]
        assert hasattr(first_prompt, 'name')
        assert hasattr(first_prompt, 'code')
        assert hasattr(first_prompt, 'scope')
        assert hasattr(first_prompt, 'params')
        assert hasattr(first_prompt, 'file')
        assert not hasattr(first_prompt, 'content')
    
    def test_get_prompt_by_code(self, service):
        """Test getting a specific prompt by code returns content."""
        prompt = service.get_prompt_by_code(1)
        
        assert prompt is not None
        assert isinstance(prompt, PromptTemplate)
        assert prompt.code == 1
        assert prompt.name == "hello"
        assert hasattr(prompt, 'content')
        assert not hasattr(prompt, 'file')
        assert "Hello, {name}! Welcome!" in prompt.content
    
    def test_get_prompt_by_invalid_code(self, service):
        """Test getting a prompt with invalid code returns None."""
        prompt = service.get_prompt_by_code(999)
        assert prompt is None

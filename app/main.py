from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from .models import PromptListResponse, PromptResponse
from .services import PromptService

app = FastAPI(
    title="File Reader API",
    description="A simple API to read local files and return prompt templates",
    version="0.1.0"
)

# Initialize the prompt service
prompt_service = PromptService()


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": "File Reader API",
        "version": "0.1.0",
        "endpoints": {
            "prompt_templates": "/api/prompt-templates"
        }
    }


@app.get("/api/prompt-templates", response_model=PromptListResponse | PromptResponse)
async def get_prompt_templates(code: Optional[int] = Query(None, description="Code to filter prompts")):
    """
    Get prompt templates.
    
    - If 'code' is provided, returns a specific prompt template with content
    - If 'code' is not provided, returns all prompt templates (metadata only)
    """
    if code is not None:
        # Return specific prompt by code
        prompt = prompt_service.get_prompt_by_code(code)
        if prompt is None:
            raise HTTPException(status_code=404, detail=f"Prompt with code {code} not found")
        
        return PromptResponse(prompt=prompt)
    else:
        # Return all prompts (metadata only)
        prompts = prompt_service.get_all_prompts()
        return PromptListResponse(prompts=prompts)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

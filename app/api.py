"""
API routes for SecurePrompt application.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .core.checker import prompt_checker


router = APIRouter()


class PromptRequest(BaseModel):
    """Request model for prompt checking."""
    prompt: str


class PromptResponse(BaseModel):
    """Response model for prompt checking."""
    status: str
    matches: list
    response: str = None


@router.post("/check", response_model=Dict[str, Any])
async def check_prompt(request: PromptRequest) -> Dict[str, Any]:
    """
    Check if a prompt contains sensitive content.
    
    Args:
        request: PromptRequest containing the prompt to check
        
    Returns:
        Dictionary with status, matches, and response (if safe)
    """
    try:
        result = prompt_checker.check_prompt(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing prompt: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "SecurePrompt API is running"}


@router.get("/keywords")
async def get_keywords():
    """Get the list of sensitive keywords being monitored."""
    return {
        "keywords": prompt_checker.aho_corasick.patterns,
        "count": len(prompt_checker.aho_corasick.patterns)
    }
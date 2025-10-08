"""
API routes for SecurePrompt application.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.error
import json
import os
import time
from .core.checker import check_prompt


router = APIRouter()


class PromptRequest(BaseModel):
    """Request model for prompt checking."""
    prompt: str


class GenerateRequest(BaseModel):
    """Request model for Ollama generate endpoint."""
    model: str = "llama3.2:latest"
    prompt: str
    stream: bool = False


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatCompletionsRequest(BaseModel):
    """OpenAI-compatible chat completions request."""
    model: str = "llama3.2:latest"
    messages: List[ChatMessage]
    stream: bool = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


@router.post("/check", response_model=Dict[str, Any])
async def check_prompt_endpoint(request: PromptRequest) -> Dict[str, Any]:
    """
    Check if a prompt contains sensitive content.
    
    Args:
        request: PromptRequest containing the prompt to check
        
    Returns:
        Dictionary with status, matches, and response (if safe)
    """
    try:
        result = check_prompt(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing prompt: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "SecurePrompt API is running"}





# Ollama configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:latest')


def call_ollama_generate(prompt: str, model: str = OLLAMA_MODEL) -> Dict[str, Any]:
    """Call Ollama generate endpoint"""
    try:
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/generate",
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except urllib.error.URLError as e:
        return {
            "error": f"Failed to connect to Ollama: {str(e)}",
            "response": f"[OLLAMA UNAVAILABLE] Mock response for: {prompt}",
            "done": True,
            "created_at": "2025-01-01T00:00:00.000Z"
        }
    except Exception as e:
        return {
            "error": f"Ollama error: {str(e)}",
            "response": f"[OLLAMA ERROR] Mock response for: {prompt}",
            "done": True,
            "created_at": "2025-01-01T00:00:00.000Z"
        }


def call_ollama_chat(messages: List[Dict[str, str]], model: str = OLLAMA_MODEL) -> Dict[str, Any]:
    """Call Ollama chat endpoint"""
    try:
        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/chat",
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except urllib.error.URLError as e:
        return {
            "error": f"Failed to connect to Ollama: {str(e)}",
            "message": {
                "role": "assistant",
                "content": f"[OLLAMA UNAVAILABLE] I understand your message, but cannot connect to the AI model currently."
            },
            "done": True,
            "created_at": "2025-01-01T00:00:00.000Z"
        }
    except Exception as e:
        return {
            "error": f"Ollama error: {str(e)}",
            "message": {
                "role": "assistant", 
                "content": f"[OLLAMA ERROR] There was an error processing your request."
            },
            "done": True,
            "created_at": "2025-01-01T00:00:00.000Z"
        }


def call_ollama_v1_chat(messages: List[Dict[str, str]], model: str = OLLAMA_MODEL) -> Dict[str, Any]:
    """Call Ollama OpenAI-compatible v1 chat completions endpoint"""
    try:
        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/v1/chat/completions",
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except urllib.error.URLError as e:
        # Return OpenAI-compatible error format
        return {
            "id": "chatcmpl-error",
            "object": "chat.completion",
            "created": 1759867723,
            "model": model,
            "system_fingerprint": "fp_secureprompt_error",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"[OLLAMA UNAVAILABLE] I understand your message, but cannot connect to the AI model currently. Error: {str(e)}"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 20,
                "total_tokens": 20
            }
        }
    except Exception as e:
        return {
            "id": "chatcmpl-error",
            "object": "chat.completion", 
            "created": 1759867723,
            "model": model,
            "system_fingerprint": "fp_secureprompt_error",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"[OLLAMA ERROR] There was an error processing your request: {str(e)}"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 15,
                "total_tokens": 15
            }
        }




def estimate_tokens(text: str) -> int:
    """Rough token estimation: ~4 characters per token"""
    return max(1, len(text) // 4)

def smart_sanitize_prompt(prompt: str, matches: List[Dict[str, Any]]) -> str:
    """Smart sanitization that completely removes sensitive context"""
    sanitized = prompt
    
    import re
    
    # More aggressive sanitization - remove entire sensitive phrases
    sanitization_patterns = [
        # Indonesian ID patterns
        (r'\b(?:NIK|nik)\s*[:\s]*\d+', 'ID'),
        (r'\b(?:NIM|nim)\s*[:\s]*\d+', 'student ID'),
        (r'\b(?:NISN|nisn)\s*[:\s]*\d+', 'student number'),
        (r'\b(?:KTP|ktp)\s*[:\s]*\d+', 'ID card'),
        
        # Phone patterns
        (r'\b(?:Phone|phone|Telepon|telepon|HP|hp)\s*[:\s]*\d+', 'phone'),
        (r'\b08\d{8,11}', 'phone'),
        (r'\b\+62\d{8,11}', 'phone'),
        
        # Email patterns
        (r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'email'),
        
        # Any remaining long numbers that might be IDs
        (r'\b\d{10,16}\b', 'ID number'),
    ]
    
    # Apply patterns
    for pattern, replacement in sanitization_patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    
    # Clean up multiple spaces and normalize
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    # Additional cleanup for common Indonesian sensitive terms
    sensitive_terms = ['NIK', 'NIM', 'NISN', 'KTP', 'nik', 'nim', 'nisn', 'ktp']
    for term in sensitive_terms:
        sanitized = sanitized.replace(f'{term}:', 'ID:')
        sanitized = sanitized.replace(f'{term} ', 'ID ')
        
    return sanitized

def sanitize_prompt(prompt: str, matches: List[Dict[str, Any]]) -> str:
    """Legacy function - kept for backwards compatibility"""
    return smart_sanitize_prompt(prompt, matches)


@router.post("/generate")
async def generate(request: GenerateRequest) -> Dict[str, Any]:
    """
    Ollama-compatible generate endpoint with security check.
    """
    try:
        # Check prompt for sensitive content
        check_result = check_prompt(request.prompt)
        
        if check_result['status'] == 'SENSITIVE':
            # BLOCK COMPLETELY - Don't send to Ollama at all
            return {
                "model": request.model,
                "created_at": "2025-10-07T21:00:00Z",
                "response": "Request blocked: This prompt contains sensitive information that cannot be processed for privacy and security reasons. Please remove any personal data and try again.",
                "done": True,
                "total_duration": 100000,
                "load_duration": 50000,  
                "prompt_eval_count": 0,
                "prompt_eval_duration": 0,
                "eval_count": 20,
                "eval_duration": 50000
            }
        else:
            # If safe, send original prompt to Ollama
            ollama_result = call_ollama_generate(request.prompt, request.model)
            
            response = {
                "model": request.model,
                "created_at": ollama_result.get("created_at", "2025-10-06T13:20:13Z"),
                "response": ollama_result.get("response", f"Safe prompt processed: {request.prompt}"),
                "done": ollama_result.get("done", True)
            }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing generate request: {str(e)}")


@router.post("/chat/completions")
async def chat_completions(request: ChatCompletionsRequest) -> Dict[str, Any]:
    """
    OpenAI-compatible chat completions endpoint with security check.
    """
    try:
        # Extract the latest user message
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            return {
                "error": {
                    "message": "No user message found in request",
                    "type": "invalid_request_error",
                    "code": "no_user_message"
                }
            }
        
        user_message = user_messages[-1].content
        
        # Security check
        check_result = check_prompt(user_message)
        
        if check_result["status"] == "SENSITIVE":
            # SMART FILTERING: Sanitize content and keep original context
            sanitized_message = smart_sanitize_prompt(user_message, check_result["matches"])
            
            # Create modified messages - preserve original system messages but sanitize user content
            modified_messages = []
            
            # Keep original system messages as they come from Moodle
            for msg in request.messages:
                if msg.role == "system":
                    modified_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
                elif msg.role == "user" and msg.content == user_message:
                    # Replace with sanitized version
                    modified_messages.append({
                        "role": "user", 
                        "content": sanitized_message
                    })
                else:
                    modified_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
                    
            messages_dict = modified_messages
        else:
            # If safe, send original conversation
            messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Call Ollama
        ollama_result = call_ollama_v1_chat(messages_dict, request.model)
        
        # Check if Ollama returned an error
        if "error" in ollama_result:
            return {
                "error": {
                    "message": ollama_result["error"],
                    "type": "server_error",
                    "code": "ollama_error"
                }
            }
        
        # Clean up response format
        completion_text = ollama_result["choices"][0]["message"]["content"]
        prompt_text = " ".join([msg.content for msg in request.messages])
        
        # Create clean OpenAI-compatible response
        clean_response = {
            "id": ollama_result.get("id", f"chatcmpl-{int(time.time())}"),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": completion_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": estimate_tokens(prompt_text),
                "completion_tokens": estimate_tokens(completion_text),
                "total_tokens": estimate_tokens(prompt_text) + estimate_tokens(completion_text)
            }
        }
        
        return clean_response
        
    except Exception as e:
        return {
            "error": {
                "message": f"Internal server error: {str(e)}",
                "type": "server_error",
                "code": "internal_error"
            }
        }



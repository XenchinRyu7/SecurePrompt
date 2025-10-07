"""
FastAPI application entry point for SecurePrompt.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router


# Get configuration from environment variables
API_TITLE = os.getenv("API_TITLE", "SecurePrompt API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "A sensitive prompt protection system using Aho-Corasick algorithm")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "SecurePrompt API",
        "description": "Sensitive prompt protection system using Aho-Corasick algorithm",
        "version": "1.0.0",
        "endpoints": {
            "check_prompt": "/api/v1/check",
            "health": "/api/v1/health", 
            "generate": "/api/v1/generate",
            "chat_completions": "/api/v1/chat/completions"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENVIRONMENT") != "production"
    uvicorn.run(app, host="0.0.0.0", port=port, reload=reload)
"""
Vercel serverless function entry point for SecurePrompt API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import our existing API
from app.api import router
from app.core.checker import prompt_checker

# Create FastAPI app
app = FastAPI(
    title="SecurePrompt API",
    description="Sensitive prompt protection system using Aho-Corasick algorithm",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SecurePrompt API",
        "description": "Sensitive prompt protection system using Aho-Corasick algorithm",
        "version": "1.0.0",
        "endpoints": {
            "check_prompt": "/api/v1/check",
            "health": "/api/v1/health",
            "keywords": "/api/v1/keywords",
            "docs": "/docs"
        }
    }

# Export handler for Vercel
handler = app
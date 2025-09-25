"""
Vercel serverless function for SecurePrompt API
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Try to import our checker, fallback if fails
try:
    from app.core.checker import prompt_checker
    print("Successfully imported prompt_checker")
except Exception as e:
    print(f"Import failed: {e}, using fallback")
    # Fallback checker
    class FallbackChecker:
        def __init__(self):
            self.keywords = ["password", "email", "phone", "nik", "credit card", "ssn", "secret", "token", "api key"]
        
        def check_prompt(self, prompt):
            if not prompt:
                return {"status": "SAFE", "matches": [], "response": "LLM response: (empty prompt)"}
            
            prompt_lower = prompt.lower()
            matches = []
            
            for keyword in self.keywords:
                pos = prompt_lower.find(keyword.lower())
                if pos != -1:
                    matches.append({
                        "keyword": keyword.lower(),
                        "position": pos
                    })
            
            if matches:
                return {"status": "SENSITIVE", "matches": matches}
            else:
                return {"status": "SAFE", "matches": [], "response": f"LLM response: {prompt}"}
    
    prompt_checker = FallbackChecker()

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/' or path == '/api':
                response = {
                    "message": "SecurePrompt API",
                    "description": "Sensitive prompt protection system using Aho-Corasick algorithm",
                    "version": "1.0.0",
                    "endpoints": {
                        "check": "/api/check",
                        "health": "/api/health",
                        "keywords": "/api/keywords"
                    }
                }
            elif path == '/api/health':
                response = {
                    "status": "healthy",
                    "message": "SecurePrompt API is running on Vercel",
                    "timestamp": "2025-09-25"
                }
            elif path == '/api/keywords':
                try:
                    if hasattr(prompt_checker, 'keywords'):
                        keywords = prompt_checker.keywords
                    elif hasattr(prompt_checker, 'aho_corasick'):
                        keywords = prompt_checker.aho_corasick.patterns
                    else:
                        keywords = ["password", "email", "phone", "nik", "credit card"]
                    
                    response = {
                        "keywords": keywords,
                        "count": len(keywords)
                    }
                except Exception as e:
                    response = {
                        "keywords": ["password", "email", "phone", "nik", "credit card"],
                        "count": 5,
                        "error": str(e)
                    }
            else:
                response = {"error": f"GET endpoint not found: {path}"}
                
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {"error": f"Internal server error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())

    def do_POST(self):
        """Handle POST requests"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/api/check':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    prompt = data.get('prompt', '')
                    
                    if not prompt:
                        response = {"error": "Prompt is required"}
                    else:
                        response = prompt_checker.check_prompt(prompt)
                else:
                    response = {"error": "No data provided"}
            else:
                response = {"error": f"POST endpoint not found: {path}"}
                
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {"error": f"Error processing request: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
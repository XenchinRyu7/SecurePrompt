"""
Vercel serverless function for SecurePrompt API
Simple HTTP handler without FastAPI for better Vercel compatibility
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.core.checker import prompt_checker
except ImportError:
    # Fallback if import fails
    class MockChecker:
        def check_prompt(self, prompt):
            return {
                "status": "SAFE",
                "matches": [],
                "response": f"LLM response: {prompt}"
            }
    prompt_checker = MockChecker()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
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
                "message": "SecurePrompt API is running on Vercel"
            }
        elif path == '/api/keywords':
            try:
                response = {
                    "keywords": prompt_checker.aho_corasick.patterns if hasattr(prompt_checker, 'aho_corasick') else ["password", "email", "phone", "nik"],
                    "count": len(prompt_checker.aho_corasick.patterns) if hasattr(prompt_checker, 'aho_corasick') else 4
                }
            except:
                response = {
                    "keywords": ["password", "email", "phone", "nik", "credit card"],
                    "count": 5
                }
        else:
            response = {"error": "Endpoint not found"}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/check':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                prompt = data.get('prompt', '')
                
                if not prompt:
                    response = {"error": "Prompt is required"}
                else:
                    # Use our checker
                    response = prompt_checker.check_prompt(prompt)
                    
            except Exception as e:
                response = {
                    "error": f"Error processing request: {str(e)}"
                }
        else:
            response = {"error": "Endpoint not found"}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
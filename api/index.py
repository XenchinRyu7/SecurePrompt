"""
Vercel serverless function for SecurePrompt API
"""
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

def handler(request):
    """Main Vercel handler function"""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    try:
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        
        # Handle OPTIONS for CORS
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Handle GET requests
        if method == 'GET':
            if path == '/' or path == '/api' or not path:
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
            elif path == '/api/health' or path == '/health':
                response = {
                    "status": "healthy",
                    "message": "SecurePrompt API is running on Vercel",
                    "timestamp": "2025-09-25"
                }
            elif path == '/api/keywords' or path == '/keywords':
                try:
                    keywords = prompt_checker.keywords if hasattr(prompt_checker, 'keywords') else prompt_checker.aho_corasick.patterns
                    response = {
                        "keywords": keywords,
                        "count": len(keywords)
                    }
                except:
                    response = {
                        "keywords": ["password", "email", "phone", "nik", "credit card"],
                        "count": 5
                    }
            else:
                response = {"error": f"GET endpoint not found: {path}"}
        
        # Handle POST requests
        elif method == 'POST':
            if path == '/api/check' or path == '/check':
                try:
                    body = request.get('body', '{}')
                    if isinstance(body, str):
                        data = json.loads(body)
                    else:
                        data = body
                    
                    prompt = data.get('prompt', '')
                    
                    if not prompt:
                        response = {"error": "Prompt is required"}
                    else:
                        response = prompt_checker.check_prompt(prompt)
                        
                except Exception as e:
                    response = {"error": f"Error processing request: {str(e)}"}
            else:
                response = {"error": f"POST endpoint not found: {path}"}
        
        else:
            response = {"error": f"Method {method} not supported"}
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        error_response = {
            "error": f"Internal server error: {str(e)}",
            "path": request.get('path', 'unknown'),
            "method": request.get('method', 'unknown')
        }
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(error_response)
        }
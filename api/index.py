"""
Vercel serverless function for SecurePrompt API
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import sys
import urllib.request
import urllib.error

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

# Ollama configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:latest')

def call_ollama_generate(prompt, model=OLLAMA_MODEL):
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
            "response": f"[OLLAMA UNAVAILABLE] Mock response for: {prompt}"
        }
    except Exception as e:
        return {
            "error": f"Ollama error: {str(e)}",
            "response": f"[OLLAMA ERROR] Mock response for: {prompt}"
        }

def call_ollama_chat(messages, model=OLLAMA_MODEL):
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
            }
        }
    except Exception as e:
        return {
            "error": f"Ollama error: {str(e)}",
            "message": {
                "role": "assistant", 
                "content": f"[OLLAMA ERROR] There was an error processing your request."
            }
        }

def sanitize_prompt(prompt, matches):
    """Sanitize prompt by replacing sensitive content with [REDACTED]"""
    sanitized = prompt
    
    # Sort matches by position in reverse order to avoid index shifting
    sorted_matches = sorted(matches, key=lambda x: x['position'], reverse=True)
    
    for match in sorted_matches:
        keyword = match['keyword']
        pos = match['position']
        # Replace the detected keyword with [REDACTED]
        before = sanitized[:pos]
        after = sanitized[pos + len(keyword):]
        sanitized = before + f"[REDACTED-{keyword.upper()}]" + after
    
    return sanitized

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
                        "keywords": "/api/keywords",
                        "generate": "/api/generate",
                        "chat": "/api/chat"
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
                    
            elif path == '/api/generate':
                # Ollama-compatible generate endpoint
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    prompt = data.get('prompt', '')
                    model = data.get('model', 'secureprompt')
                    stream = data.get('stream', False)
                    
                    if not prompt:
                        response = {"error": "Prompt is required"}
                    else:
                        # Check prompt for sensitive content
                        check_result = prompt_checker.check_prompt(prompt)
                        
                        if check_result['status'] == 'SENSITIVE':
                            # Sanitize the prompt by replacing sensitive content
                            sanitized_prompt = sanitize_prompt(prompt, check_result['matches'])
                            
                            # Send sanitized prompt to Ollama
                            ollama_result = call_ollama_generate(sanitized_prompt, model)
                            
                            # Build response with security info
                            response = {
                                "model": model,
                                "created_at": ollama_result.get("created_at", "2025-01-01T00:00:00.000Z"),
                                "response": ollama_result.get("response", f"[REDACTED] Sensitive content detected and sanitized before processing."),
                                "done": ollama_result.get("done", True),
                                "context": ollama_result.get("context", []),
                                "total_duration": ollama_result.get("total_duration", 1000000),
                                "load_duration": ollama_result.get("load_duration", 500000),
                                "prompt_eval_count": ollama_result.get("prompt_eval_count", len(sanitized_prompt.split())),
                                "prompt_eval_duration": ollama_result.get("prompt_eval_duration", 300000),
                                "eval_count": ollama_result.get("eval_count", 10),
                                "eval_duration": ollama_result.get("eval_duration", 200000),
                                "security_check": {
                                    "status": "SENSITIVE_SANITIZED",
                                    "matches": check_result['matches'],
                                    "sanitized_prompt": sanitized_prompt,
                                    "original_prompt": prompt
                                }
                            }
                            
                            # Add Ollama error info if present
                            if "error" in ollama_result:
                                response["ollama_error"] = ollama_result["error"]
                        else:
                            # If safe, send original prompt to Ollama
                            ollama_result = call_ollama_generate(prompt, model)
                            
                            response = {
                                "model": model,
                                "created_at": ollama_result.get("created_at", "2025-01-01T00:00:00.000Z"),
                                "response": ollama_result.get("response", f"Safe prompt processed: {prompt}"),
                                "done": ollama_result.get("done", True),
                                "context": ollama_result.get("context", []),
                                "total_duration": ollama_result.get("total_duration", 1500000),
                                "load_duration": ollama_result.get("load_duration", 500000),
                                "prompt_eval_count": ollama_result.get("prompt_eval_count", len(prompt.split())),
                                "prompt_eval_duration": ollama_result.get("prompt_eval_duration", 800000),
                                "eval_count": ollama_result.get("eval_count", 15),
                                "eval_duration": ollama_result.get("eval_duration", 700000),
                                "security_check": {
                                    "status": "SAFE",
                                    "matches": []
                                }
                            }
                            
                            # Add Ollama error info if present
                            if "error" in ollama_result:
                                response["ollama_error"] = ollama_result["error"]
                else:
                    response = {"error": "No data provided"}
                    
            elif path == '/api/chat':
                # Ollama-compatible chat endpoint
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    messages = data.get('messages', [])
                    model = data.get('model', 'secureprompt')
                    stream = data.get('stream', False)
                    
                    if not messages:
                        response = {"error": "Messages are required"}
                    else:
                        # Extract the latest user message
                        user_message = ""
                        for msg in reversed(messages):
                            if msg.get('role') == 'user':
                                user_message = msg.get('content', '')
                                break
                        
                        if not user_message:
                            response = {"error": "No user message found"}
                        else:
                            # Check prompt for sensitive content
                            check_result = prompt_checker.check_prompt(user_message)
                            
                            if check_result['status'] == 'SENSITIVE':
                                # Sanitize the user message
                                sanitized_message = sanitize_prompt(user_message, check_result['matches'])
                                
                                # Create sanitized messages array
                                sanitized_messages = []
                                for msg in messages:
                                    if msg.get('role') == 'user' and msg.get('content') == user_message:
                                        sanitized_messages.append({
                                            "role": "user",
                                            "content": sanitized_message
                                        })
                                    else:
                                        sanitized_messages.append(msg)
                                
                                # Send sanitized conversation to Ollama
                                ollama_result = call_ollama_chat(sanitized_messages, model)
                                
                                response = {
                                    "model": model,
                                    "created_at": ollama_result.get("created_at", "2025-01-01T00:00:00.000Z"),
                                    "message": ollama_result.get("message", {
                                        "role": "assistant",
                                        "content": "Your message contained sensitive information which has been sanitized before processing."
                                    }),
                                    "done": ollama_result.get("done", True),
                                    "total_duration": ollama_result.get("total_duration", 1500000),
                                    "load_duration": ollama_result.get("load_duration", 500000),
                                    "prompt_eval_count": ollama_result.get("prompt_eval_count", len(sanitized_message.split())),
                                    "prompt_eval_duration": ollama_result.get("prompt_eval_duration", 800000),
                                    "eval_count": ollama_result.get("eval_count", 10),
                                    "eval_duration": ollama_result.get("eval_duration", 700000),
                                    "security_check": {
                                        "status": "SENSITIVE_SANITIZED",
                                        "matches": check_result['matches'],
                                        "sanitized_message": sanitized_message,
                                        "original_message": user_message
                                    }
                                }
                                
                                # Add Ollama error info if present
                                if "error" in ollama_result:
                                    response["ollama_error"] = ollama_result["error"]
                            else:
                                # If safe, send original conversation to Ollama
                                ollama_result = call_ollama_chat(messages, model)
                                
                                response = {
                                    "model": model,
                                    "created_at": ollama_result.get("created_at", "2025-01-01T00:00:00.000Z"),
                                    "message": ollama_result.get("message", {
                                        "role": "assistant",
                                        "content": f"Safe conversation processed."
                                    }),
                                    "done": ollama_result.get("done", True),
                                    "total_duration": ollama_result.get("total_duration", 1500000),
                                    "load_duration": ollama_result.get("load_duration", 500000),
                                    "prompt_eval_count": ollama_result.get("prompt_eval_count", len(user_message.split())),
                                    "prompt_eval_duration": ollama_result.get("prompt_eval_duration", 800000),
                                    "eval_count": ollama_result.get("eval_count", 15),
                                    "eval_duration": ollama_result.get("eval_duration", 700000),
                                    "security_check": {
                                        "status": "SAFE",
                                        "matches": []
                                    }
                                }
                                
                                # Add Ollama error info if present
                                if "error" in ollama_result:
                                    response["ollama_error"] = ollama_result["error"]
                else:
                    response = {"error": "No data provided"}
                    
            else:
                response = {"error": f"POST endpoint not found: {path}"}
                
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {"error": f"Error processing request: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
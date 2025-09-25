# SecurePrompt - Sensitive Prompt Protection System

A FastAPI-based application that detects sensitive content in user prompts using a custom implementation of the Aho-Corasick string matching algorithm.

## Features

- **Custom Aho-Corasick Implementation**: Built from scratch without external Aho-Corasick libraries
- **Sensitive Content Detection**: Identifies keywords like NIK, email, phone, password, credit card, etc.
- **Case-Insensitive Matching**: Detects sensitive content regardless of case
- **FastAPI REST API**: Clean API endpoints for prompt checking
- **Comprehensive Testing**: Full test suite with pytest
- **Real-time Protection**: Blocks sensitive prompts and provides detailed match information

## Project Structure

```
app/
├── main.py              # FastAPI entry point
├── api.py               # API routes
├── core/
│   ├── __init__.py
│   ├── aho_corasick.py  # Manual Aho-Corasick implementation
│   └── checker.py       # check_prompt logic + dummy LLM forward
└── tests/
    └── test_checker.py  # Example test cases
```

## Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows (PowerShell):
     ```powershell
     venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```cmd
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the API server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST `/api/v1/check`
Check if a prompt contains sensitive content.

**Request Body:**
```json
{
  "prompt": "What is my password?"
}
```

**Response (Sensitive):**
```json
{
  "status": "SENSITIVE",
  "matches": [
    {
      "keyword": "password",
      "position": 10
    }
  ]
}
```

**Response (Safe):**
```json
{
  "status": "SAFE",
  "matches": [],
  "response": "LLM response: What is the weather today?"
}
```

### GET `/api/v1/health`
Health check endpoint.

### GET `/api/v1/keywords`
Get the list of monitored sensitive keywords.

## Running Tests

Run the test suite:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests with coverage:
```bash
pytest --cov=app
```

## Algorithm Details

### Aho-Corasick Implementation

The core algorithm consists of three main phases:

1. **Trie Construction**: Build a trie (prefix tree) from all sensitive keywords
2. **Failure Link Construction**: Create failure links for efficient pattern matching using BFS
3. **Pattern Matching**: Scan input text character by character, following failure links when necessary

### Sensitive Keywords

Default sensitive keywords include:
- NIK (Indonesian National ID)
- email
- phone
- password
- credit card
- ssn
- social security
- bank account
- pin
- cvv
- passport
- driver license
- api key
- token
- secret
- private key
- confidential
- classified

## Usage Examples

### Python Code Example:
```python
from app.core.checker import PromptChecker

# Create checker instance
checker = PromptChecker()

# Check a safe prompt
result = checker.check_prompt("What is the weather today?")
print(result)  # {"status": "SAFE", "matches": [], "response": "LLM response: ..."}

# Check a sensitive prompt
result = checker.check_prompt("My password is secret123")
print(result)  # {"status": "SENSITIVE", "matches": [{"keyword": "password", "position": 3}]}
```

### cURL Example:
```bash
# Check a prompt
curl -X POST "http://localhost:8000/api/v1/check" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is my password?"}'
```

## Development

### Project Setup for Development:
1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `pytest`
5. Start development server: `uvicorn app.main:app --reload`

### Adding New Sensitive Keywords:
Modify the `DEFAULT_SENSITIVE_KEYWORDS` list in `app/core/checker.py` or create a custom `PromptChecker` instance with your own keyword list.

## Security Considerations

- The system performs case-insensitive matching
- All patterns are converted to lowercase for consistent matching
- The system blocks prompts containing any sensitive keywords
- In production, consider additional security measures like rate limiting and authentication

## Deployment

### Quick Deploy Options

#### 1. Railway (Recommended) ⭐
```bash
# Push to GitHub first
git init && git add . && git commit -m "Initial commit"

# Deploy to Railway
# 1. Go to railway.app
# 2. Connect GitHub repo
# 3. Auto-deploy!
```

#### 2. Render
```bash
# Connect GitHub repo at render.com
# Build command: pip install -r requirements.txt
# Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 3. Docker
```bash
# Build and run locally
docker build -t secureprompt .
docker run -p 8000:8000 secureprompt
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Live Demo
Once deployed, your API will be available at:
- Health check: `GET /api/v1/health`
- API docs: `GET /docs`
- Check prompt: `POST /api/v1/check`

## License

This project is for educational purposes as part of a thesis project.
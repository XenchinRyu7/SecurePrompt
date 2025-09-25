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

#### 1. Vercel (Recommended) ⭐
```bash
# Push to GitHub first (sudah done!)
# Deploy to Vercel
# 1. Go to vercel.com (NO CREDIT CARD NEEDED!)
# 2. Continue with GitHub
# 3. Import repo: XenchinRyu7/SecurePrompt
# 4. Deploy! (1-2 menit)
```

#### 2. Render.com
```bash
# Free tier but needs credit card verification
# 750 hours/month, sleep after 15min idle
```

#### 3. Docker
```bash
# Build and run locally
docker build -t secureprompt .
docker run -p 8000:8000 secureprompt
```

**📖 Detailed Guides:**
- [Vercel Deploy Guide](VERCEL_DEPLOY.md) - Recommended (No Credit Card!)
- [General Deployment Options](DEPLOYMENT.md)

### Live Demo
🌟 **API is LIVE at: https://secure-prompt.vercel.app**

Available endpoints:
- Health check: `GET /api/health`
- Keywords list: `GET /api/keywords`  
- Check prompt: `POST /api/check`
- API root: `GET /`

## 🤝 Contributing

We welcome contributions! SecurePrompt is an open-source project and we'd love to have you contribute.

### Quick Start for Contributors
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes and add tests
4. **Ensure** all tests pass: `pytest app/tests/`
5. **Submit** a pull request

### Areas We Need Help With
- 🚀 **Performance optimization** of Aho-Corasick algorithm
- 🌐 **Additional language support** for keyword detection
- 📊 **Benchmarking** and performance metrics
- 📖 **Documentation** improvements
- 🐛 **Bug fixes** and edge cases

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ **Commercial use** allowed
- ✅ **Modification** allowed  
- ✅ **Distribution** allowed
- ✅ **Private use** allowed
- ❗ **No warranty** provided
- ❗ **License and copyright** notice required

## 🙏 Acknowledgments

- **Aho-Corasick Algorithm** - Alfred V. Aho and Margaret J. Corasick (1975)
- **FastAPI** - Sebastian Ramirez and contributors
- **Vercel** - For free serverless hosting
- **Open Source Community** - For inspiration and support

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/XenchinRyu7/SecurePrompt/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/XenchinRyu7/SecurePrompt/discussions)
- 📧 **Contact**: [@XenchinRyu7](https://github.com/XenchinRyu7)

---

## 🌟 Show Your Support

If this project helped you, please consider:
- ⭐ **Starring** the repository
- 🍴 **Forking** and contributing
- 📢 **Sharing** with others
- 💖 **Sponsoring** development

---

**Made with ❤️ for secure AI applications**

*SecurePrompt - Protecting sensitive information in AI prompts since 2025* 🛡️
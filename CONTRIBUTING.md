# Contributing to SecurePrompt

Thank you for your interest in contributing to SecurePrompt! 🎉

SecurePrompt is an open-source sensitive prompt protection system using a custom Aho-Corasick algorithm implementation. We welcome contributions from the community.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/SecurePrompt.git`
3. **Create** a new branch: `git checkout -b feature/your-feature-name`
4. **Set up** the development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow **PEP 8** Python style guide
- Use **type hints** where possible
- Add **docstrings** to functions and classes
- Keep functions **small and focused**

### Testing
- All new features must include **unit tests**
- Run tests before submitting: `pytest app/tests/`
- Ensure **19/19 tests pass**
- Add new tests for new functionality

### Algorithm Implementation
- **No external Aho-Corasick libraries** - we implement from scratch
- Maintain **O(n + m + z)** time complexity where:
  - n = text length
  - m = total pattern length  
  - z = number of matches
- Document algorithm changes thoroughly

## 📝 How to Contribute

### 🐛 Bug Reports
When reporting bugs, please include:
- **Python version** and OS
- **Error message** and stack trace
- **Steps to reproduce** the issue
- **Expected vs actual behavior**

### ✨ Feature Requests
For new features, please:
- **Check existing issues** first
- **Describe the use case** clearly
- **Explain the benefit** to users
- **Consider implementation complexity**

### 🔧 Pull Requests

1. **Create an issue** first to discuss major changes
2. **Write clear commit messages**:
   ```
   feat: add support for regex patterns in keywords
   fix: resolve memory leak in trie construction  
   docs: update API documentation
   test: add edge cases for empty input
   ```
3. **Update documentation** if needed
4. **Add/update tests** for your changes
5. **Ensure all tests pass**

### 📋 Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows PEP 8 style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🎯 Areas for Contribution

### High Priority
- **Performance optimization** of Aho-Corasick algorithm
- **Memory usage reduction** for large keyword sets
- **Additional language support** (keyword detection in other languages)
- **Benchmark testing** and performance metrics

### Medium Priority  
- **Web interface** for testing the API
- **Keyword management** API endpoints (add/remove keywords)
- **Configuration file** support for custom keywords
- **Docker optimization** for smaller image size

### Documentation
- **API documentation** improvements
- **Algorithm explanation** with diagrams
- **Usage examples** in different languages
- **Performance tuning** guide

## 🧪 Testing Your Changes

### Local Testing
```bash
# Run all tests
pytest app/tests/ -v

# Run specific test
pytest app/tests/test_checker.py::test_safe_prompt -v

# Test API locally
uvicorn app.main:app --reload
python test_deployed_api.py http://localhost:8000
```

### API Testing
```bash
# Test the live API
python test_deployed_api.py https://secure-prompt.vercel.app
```

## 📚 Resources

### Algorithm Reference
- **Aho-Corasick Algorithm**: [Original paper](https://dl.acm.org/doi/10.1145/360825.360855)
- **Implementation details**: See `app/core/aho_corasick.py`
- **Time complexity**: O(n + m + z) explanation in code comments

### API Reference
- **FastAPI docs**: https://fastapi.tiangolo.com/
- **Live API**: https://secure-prompt.vercel.app
- **API endpoints**: Check `app/api.py`

## 🤝 Community

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Share knowledge** and best practices
- **Collaborate constructively**

## 📋 Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request  
- `documentation` - Improvements to docs
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `algorithm` - Core Aho-Corasick implementation
- `api` - FastAPI related changes
- `performance` - Performance improvements
- `security` - Security related issues

## 🎉 Recognition

Contributors will be:
- **Listed** in the README.md
- **Credited** in release notes
- **Appreciated** by the community!

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/XenchinRyu7/SecurePrompt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/XenchinRyu7/SecurePrompt/discussions)
- **Maintainer**: [@XenchinRyu7](https://github.com/XenchinRyu7)

---

## 🚀 Ready to Contribute?

1. **Star** ⭐ the repository if you find it useful
2. **Fork** 🍴 and start contributing
3. **Share** 📢 with others who might be interested

Thank you for making SecurePrompt better! 🙏

---

*Happy coding! 🎯*
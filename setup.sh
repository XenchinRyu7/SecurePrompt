#!/bin/bash
# Quick setup script for SecurePrompt

echo "🔐 SecurePrompt Setup Script"
echo "=============================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "⬇️  Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python -m pytest app/tests/ -v

# Test direct functionality
echo "🔍 Testing direct functionality..."
python simple_test.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the server:"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "📖 API Documentation will be available at:"
echo "   http://localhost:8000/docs"
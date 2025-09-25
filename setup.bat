@echo off
REM Quick setup script for SecurePrompt (Windows)

echo 🔐 SecurePrompt Setup Script
echo ==============================

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo ⬇️  Installing dependencies...
pip install -r requirements.txt

REM Run tests
echo 🧪 Running tests...
python -m pytest app/tests/ -v

REM Test direct functionality
echo 🔍 Testing direct functionality...
python simple_test.py

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start the server:
echo    venv\Scripts\activate.bat
echo    uvicorn app.main:app --reload
echo.
echo 📖 API Documentation will be available at:
echo    http://localhost:8000/docs
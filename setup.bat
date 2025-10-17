@echo off
echo ========================================
echo      SecurePrompt Setup Script
echo ========================================
echo.

REM Check Python installation
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ and add it to your PATH.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Display Python version
python --version

REM Create virtual environment
echo [INFO] Creating virtual environment...
if exist "venv" (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

REM Test installation
echo [INFO] Testing installation...
python -c "from app.main import app; print('✅ SecurePrompt installation successful!')"
if %errorlevel% neq 0 (
    echo [ERROR] Installation test failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Run 'run.bat' to start the server
echo 2. Visit http://127.0.0.1:8000/docs for API documentation
echo 3. Test with http://127.0.0.1:8000/api/v1/health
echo.
echo For Moodle integration use:
echo - URL: http://127.0.0.1:8000/api/v1/chat/completions
echo - Model: llama3.2:latest
echo - Format: OpenAI ChatGPT compatible
echo.
deactivate
pause
@echo off
echo ========================================
echo       SecurePrompt Server Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to create the virtual environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if required packages are installed
echo [INFO] Checking dependencies...
python -c "import fastapi, uvicorn" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Required packages not installed!
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)

REM Start the server
echo [INFO] Starting SecurePrompt server...
echo [INFO] Server will be available at: http://127.0.0.1:8000
echo [INFO] API Documentation: http://127.0.0.1:8000/docs
echo [INFO] Health Check: http://127.0.0.1:8000/api/v1/health
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

REM Deactivate virtual environment when server stops
echo.
echo [INFO] Server stopped. Deactivating virtual environment...
deactivate
echo [INFO] Done!
pause
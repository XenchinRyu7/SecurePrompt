@echo off
REM Build and test Docker deployment locally (Windows)

echo 🐳 Building Docker image...
docker build -t secureprompt .

echo 🚀 Starting container on port 8000...
docker run -p 8000:8000 --name secureprompt-test secureprompt
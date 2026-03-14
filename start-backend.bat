@echo off
echo =========================================
echo   AI4Alzheimers - Backend Server
echo =========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
pip install -q fastapi uvicorn torch torchvision pillow python-multipart

echo.
echo Checking for model file...
if not exist "..\models\best_model.pt" (
    echo WARNING: Model file not found at ..\models\best_model.pt
    echo Please ensure your trained model is in the correct location
    echo.
)

echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn server:app --reload --port 8000

pause

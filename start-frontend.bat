@echo off
echo =========================================
echo   AI4Alzheimers - Frontend App
echo =========================================
echo.

cd /d "%~dp0"

echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16 or higher from https://nodejs.org
    pause
    exit /b 1
)

echo.
echo Installing dependencies (this may take a few minutes)...
call npm install

echo.
echo Starting development server...
echo The app will open at http://localhost:5173
echo Press Ctrl+C to stop the server
echo.
call npm run dev

pause

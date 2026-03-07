@echo off
echo ========================================
echo   EMOTION CIPHER - Quick Deploy Setup
echo ========================================
echo.

REM Check if ngrok is installed
where ngrok >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ngrok is not installed!
    echo.
    echo Please install ngrok:
    echo 1. Download from https://ngrok.com/download
    echo 2. Extract and add to PATH
    echo 3. Sign up at https://dashboard.ngrok.com/signup
    echo 4. Run: ngrok config add-authtoken YOUR_TOKEN
    echo.
    pause
    exit /b 1
)

echo [1/3] Starting backend server...
echo.

REM Start backend in a new window
start "EMOTION CIPHER Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] Starting ngrok tunnel...
echo.

REM Start ngrok in a new window
start "EMOTION CIPHER ngrok" cmd /k "ngrok http 8000"

echo.
echo [3/3] Setup complete!
echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Look at the ngrok window
echo 2. Copy the HTTPS URL (e.g., https://abc123.ngrok-free.app)
echo 3. Go to Vercel project settings
echo 4. Update NEXT_PUBLIC_API_URL environment variable
echo 5. Redeploy your Vercel app
echo.
echo Your backend is now accessible from the internet!
echo.
pause

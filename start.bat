@echo off
REM EMOTION CIPHER - Startup Script for Windows

echo 🎭 Starting EMOTION CIPHER...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10 or higher.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18 or higher.
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Backend setup
echo 🔧 Setting up backend...
cd backend

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

echo ✅ Backend setup complete
echo.

REM Frontend setup
echo 🔧 Setting up frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local...
    copy .env.local.example .env.local
)

echo ✅ Frontend setup complete
echo.

REM Start services
echo 🚀 Starting services...
echo.

REM Start backend
cd ..\backend
echo Starting backend on http://localhost:8000...
start cmd /k "venv\Scripts\activate.bat && uvicorn src.main:app --reload"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
cd ..\frontend
echo Starting frontend on http://localhost:3000...
start cmd /k "npm run dev"

echo.
echo ✨ EMOTION CIPHER is running!
echo.
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend API: http://localhost:8000
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the services
echo.

pause

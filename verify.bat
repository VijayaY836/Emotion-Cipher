@echo off
REM EMOTION CIPHER - Installation Verification Script

echo 🔍 Verifying EMOTION CIPHER Installation...
echo.

set ERRORS=0

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python %PYTHON_VERSION% installed
) else (
    echo ❌ Python not found
    set /a ERRORS+=1
)

REM Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ Node.js %NODE_VERSION% installed
) else (
    echo ❌ Node.js not found
    set /a ERRORS+=1
)

REM Check npm
echo Checking npm...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f %%i in ('npm --version') do set NPM_VERSION=%%i
    echo ✅ npm %NPM_VERSION% installed
) else (
    echo ❌ npm not found
    set /a ERRORS+=1
)

echo.
echo Checking project structure...

REM Check backend files
if exist "backend\requirements.txt" (
    echo ✅ Backend requirements.txt found
) else (
    echo ❌ Backend requirements.txt missing
    set /a ERRORS+=1
)

if exist "backend\src\main.py" (
    echo ✅ Backend main.py found
) else (
    echo ❌ Backend main.py missing
    set /a ERRORS+=1
)

REM Check frontend files
if exist "frontend\package.json" (
    echo ✅ Frontend package.json found
) else (
    echo ❌ Frontend package.json missing
    set /a ERRORS+=1
)

if exist "frontend\app\page.tsx" (
    echo ✅ Frontend page.tsx found
) else (
    echo ❌ Frontend page.tsx missing
    set /a ERRORS+=1
)

echo.
echo Checking documentation...

if exist "README.md" (echo ✅ README.md found) else (echo ❌ README.md missing & set /a ERRORS+=1)
if exist "QUICKSTART.md" (echo ✅ QUICKSTART.md found) else (echo ❌ QUICKSTART.md missing & set /a ERRORS+=1)
if exist "ARCHITECTURE.md" (echo ✅ ARCHITECTURE.md found) else (echo ❌ ARCHITECTURE.md missing & set /a ERRORS+=1)
if exist "DEMO.md" (echo ✅ DEMO.md found) else (echo ❌ DEMO.md missing & set /a ERRORS+=1)
if exist "LICENSE" (echo ✅ LICENSE found) else (echo ❌ LICENSE missing & set /a ERRORS+=1)

echo.
echo Checking startup scripts...

if exist "start.sh" (
    echo ✅ start.sh found
) else (
    echo ❌ start.sh missing
    set /a ERRORS+=1
)

if exist "start.bat" (
    echo ✅ start.bat found
) else (
    echo ❌ start.bat missing
    set /a ERRORS+=1
)

echo.
echo ═══════════════════════════════════════

if %ERRORS% equ 0 (
    echo ✅ All checks passed!
    echo.
    echo 🚀 Ready to start EMOTION CIPHER
    echo.
    echo Run: start.bat
) else (
    echo ❌ %ERRORS% error^(s^) found
    echo.
    echo Please fix the errors above before starting
)

echo ═══════════════════════════════════════
echo.
pause

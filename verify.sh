#!/bin/bash

# EMOTION CIPHER - Installation Verification Script

echo "🔍 Verifying EMOTION CIPHER Installation..."
echo ""

ERRORS=0

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python $PYTHON_VERSION installed"
else
    echo "❌ Python 3 not found"
    ERRORS=$((ERRORS + 1))
fi

# Check Node.js
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js $NODE_VERSION installed"
else
    echo "❌ Node.js not found"
    ERRORS=$((ERRORS + 1))
fi

# Check npm
echo "Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm $NPM_VERSION installed"
else
    echo "❌ npm not found"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "Checking project structure..."

# Check backend files
if [ -f "backend/requirements.txt" ]; then
    echo "✅ Backend requirements.txt found"
else
    echo "❌ Backend requirements.txt missing"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "backend/src/main.py" ]; then
    echo "✅ Backend main.py found"
else
    echo "❌ Backend main.py missing"
    ERRORS=$((ERRORS + 1))
fi

# Check frontend files
if [ -f "frontend/package.json" ]; then
    echo "✅ Frontend package.json found"
else
    echo "❌ Frontend package.json missing"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "frontend/app/page.tsx" ]; then
    echo "✅ Frontend page.tsx found"
else
    echo "❌ Frontend page.tsx missing"
    ERRORS=$((ERRORS + 1))
fi

# Check documentation
echo ""
echo "Checking documentation..."

DOCS=("README.md" "QUICKSTART.md" "ARCHITECTURE.md" "DEMO.md" "LICENSE")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "✅ $doc found"
    else
        echo "❌ $doc missing"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "Checking startup scripts..."

if [ -f "start.sh" ]; then
    echo "✅ start.sh found"
    if [ -x "start.sh" ]; then
        echo "✅ start.sh is executable"
    else
        echo "⚠️  start.sh is not executable (run: chmod +x start.sh)"
    fi
else
    echo "❌ start.sh missing"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "start.bat" ]; then
    echo "✅ start.bat found"
else
    echo "❌ start.bat missing"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed!"
    echo ""
    echo "🚀 Ready to start EMOTION CIPHER"
    echo ""
    echo "Run: ./start.sh (Linux/Mac) or start.bat (Windows)"
else
    echo "❌ $ERRORS error(s) found"
    echo ""
    echo "Please fix the errors above before starting"
fi

echo "═══════════════════════════════════════"

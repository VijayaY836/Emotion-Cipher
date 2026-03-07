# 🚀 EMOTION CIPHER - Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** (optional) - [Download](https://git-scm.com/)

## Installation

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

The script will:
1. Check prerequisites
2. Set up Python virtual environment
3. Install all dependencies
4. Start both backend and frontend
5. Open the application in your browser

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn src.main:app --reload
```

Backend will run on `http://localhost:8000`

#### Frontend Setup

```bash
cd frontend
npm install

# Create environment file
cp .env.local.example .env.local

# Start frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## First Run

1. **Open your browser** to `http://localhost:3000`
2. **Write a message** - Type any text you want to encrypt
3. **Enter a secret key** - This will be used for encryption
4. **Click "Encrypt Message"** - Watch the AI analyze emotions!
5. **View results** - See your encrypted message with emotion visualization
6. **Copy the encrypted packet** - Share it securely
7. **Try decryption** - Switch to decrypt mode and paste the packet

## Testing the Application

### Try These Examples

**Happy Message:**
```
I'm so excited about this project! It's going to be amazing!
```

**Sad Message:**
```
I miss the old days when things were simpler and easier.
```

**Angry Message:**
```
This is completely unacceptable and I'm very frustrated!
```

**Mixed Emotions:**
```
I'm nervous but also excited about the presentation tomorrow.
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### Backend Issues

**Model download taking too long?**
- First run downloads ~250MB model from HuggingFace
- Subsequent runs use cached model
- Check your internet connection

**Port 8000 already in use?**
```bash
# Find and kill the process
# Linux/Mac:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**Port 3000 already in use?**
```bash
# The dev server will automatically try port 3001
# Or kill the process:
# Linux/Mac:
lsof -ti:3000 | xargs kill -9
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Dependencies not installing?**
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Development

### Running Tests

**Backend:**
```bash
cd backend
pytest tests/ --cov=src
```

**Frontend:**
```bash
cd frontend
npm test
```

### Code Formatting

**Backend:**
```bash
cd backend
black src/
```

**Frontend:**
```bash
cd frontend
npm run lint
```

## Architecture Overview

```
EMOTION CIPHER
├── backend/          # Python FastAPI
│   ├── src/         # Source code
│   │   ├── main.py              # API endpoints
│   │   ├── emotion_detector.py  # AI emotion detection
│   │   ├── emotion_encoder.py   # Emotion hashing
│   │   ├── encryption_engine.py # AES-256 encryption
│   │   └── decryptor.py         # Decryption & verification
│   └── tests/       # Test suite
│
└── frontend/        # Next.js React
    ├── app/         # Pages
    ├── components/  # UI components
    └── lib/         # Utilities & API client
```

## Next Steps

- 📖 Read the full [README.md](README.md)
- 🎨 Explore the glassmorphism UI
- 🧪 Run the test suite
- 🔬 Check out the API documentation
- 🎭 Experiment with different emotions

## Support

Having issues? Check:
1. Python version: `python --version` (should be 3.10+)
2. Node version: `node --version` (should be 18+)
3. Backend logs in the terminal
4. Browser console for frontend errors

---

**Built with ❤️ for hackathons** 🏆

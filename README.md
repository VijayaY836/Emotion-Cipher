# 🎭 EMOTION CIPHER

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

**Encrypt your messages with emotions. Decrypt with feelings.**

A revolutionary privacy-preserving communication system that encrypts text messages while maintaining their emotional signature. Built for hackathons, designed to win.

[Quick Start](QUICKSTART.md) • [Architecture](ARCHITECTURE.md) • [Demo Script](DEMO.md)

## ✨ Features

- 🧠 **AI-Powered Emotion Detection** - Uses state-of-the-art NLP to analyze emotional content
- 🔐 **Emotion-Aware Encryption** - AES-256 encryption influenced by emotional signatures
- 🎨 **Stunning Glassmorphism UI** - Beautiful, modern interface with smooth animations
- 📊 **Real-Time Emotion Visualization** - Interactive charts and animated emotion displays
- 🔒 **Privacy-First Design** - Analyze emotions without revealing message content
- ⚡ **Lightning Fast** - Optimized for performance with GPU acceleration

## 🚀 Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## 🎯 How It Works

1. **Write Your Message** - Enter any text message
2. **Emotion Analysis** - AI detects joy, sadness, anger, fear, surprise, and anxiety
3. **Emotion-Aware Encryption** - Your message is encrypted with AES-256, where the encryption key is influenced by the emotional signature
4. **Share Securely** - Send the encrypted packet to anyone
5. **Decrypt & Verify** - Recipients decrypt with the secret key and verify emotional authenticity

## 🏗️ Architecture

- **Backend**: Python FastAPI + HuggingFace Transformers + PyCryptodome
- **Frontend**: Next.js 14 + React + TypeScript + TailwindCSS + Framer Motion
- **ML Model**: `j-hartmann/emotion-english-distilroberta-base`
- **Encryption**: AES-256-CBC with emotion-aware key derivation

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ --cov=src --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test -- --coverage
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/encrypt` - Encrypt a message with emotion-aware encryption
- `POST /api/decrypt` - Decrypt and verify emotional authenticity
- `POST /api/analyze` - Analyze emotions without encryption

## 🎨 UI Highlights

- **Glassmorphism Design** - Frosted glass effects with backdrop blur
- **Smooth Animations** - Powered by Framer Motion
- **Emotion Visualizations** - Interactive bars, radar charts, and color auras
- **Responsive Layout** - Works beautifully on all devices

## 🔬 Technology Stack

**Backend:**
- FastAPI 0.104+
- HuggingFace Transformers 4.35+
- PyTorch 2.1+
- PyCryptodome 3.19+
- Hypothesis (property-based testing)

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript 5
- TailwindCSS 3.4
- Framer Motion 10
- Recharts 2.10
- fast-check (property-based testing)

## 🏆 Hackathon Ready

This project includes:
- ✅ Complete functionality
- ✅ Beautiful UI with animations
- ✅ Comprehensive testing (21 property-based tests)
- ✅ Clean, modular code
- ✅ Full documentation
- ✅ Production-ready architecture

## 📖 Use Cases

- **Mental Health Platforms** - Monitor emotional wellbeing without reading private messages
- **Anonymous Feedback** - Collect emotional sentiment while preserving anonymity
- **Workplace Analytics** - Track team morale without invading privacy
- **Secure Communication** - Add emotional context to encrypted messages

## 🤝 Contributing

This is a hackathon project built to showcase emotion-aware encryption. Feel free to fork and extend!

## 📄 License

MIT License - Built with ❤️ for hackathons

---

**Made with emotion by the EMOTION CIPHER team** 🎭✨

# 🏗️ EMOTION CIPHER - Architecture Documentation

## System Overview

EMOTION CIPHER is a full-stack web application that implements emotion-aware encryption. The system combines natural language processing (NLP) with cryptography to create a unique privacy-preserving communication system where emotional signatures influence the encryption process.

## Core Innovation

Traditional encryption treats all messages identically. EMOTION CIPHER introduces **emotion-aware key derivation**: the emotional signature of a message directly influences the encryption key, ensuring that:

1. Identical messages with different emotions produce different ciphertexts
2. Emotional metadata can be analyzed without decrypting the message
3. Emotional authenticity can be verified after decryption

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (Next.js + React)                         │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Message    │  │   Emotion    │  │  Encryption  │     │
│  │    Input     │→ │   Analysis   │→ │    Result    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  Decryption  │→ │  Verification│                        │
│  │    Input     │  │    Result    │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/JSON
┌─────────────────────────────────────────────────────────────┐
│                         Backend                              │
│                      (FastAPI + Python)                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Emotion    │→ │   Emotion    │→ │  Encryption  │     │
│  │   Detector   │  │   Encoder    │  │    Engine    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                                      ↓             │
│  ┌──────────────┐                    ┌──────────────┐     │
│  │  Decryption  │←───────────────────│  Encrypted   │     │
│  │    Module    │                    │    Packet    │     │
│  └──────────────┘                    └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         HuggingFace Model Hub                        │  │
│  │  j-hartmann/emotion-english-distilroberta-base       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Component Breakdown

#### 1. Emotion Detector (`emotion_detector.py`)

**Purpose**: Analyzes text and extracts emotional content using a pretrained transformer model.

**Key Features**:
- Uses `j-hartmann/emotion-english-distilroberta-base` from HuggingFace
- Detects 6 emotions: joy, sadness, anger, fear, surprise, anxiety
- GPU acceleration when available
- Model caching for performance
- Handles edge cases (empty input, long text)

**Flow**:
```
Text Input → Tokenization → Model Inference → Softmax → Normalization → EmotionVector
```

#### 2. Emotion Encoder (`emotion_encoder.py`)

**Purpose**: Transforms emotion vectors into cryptographic signatures.

**Key Features**:
- Deterministic emotion hashing (SHA-256)
- Dominant emotion extraction with threshold
- Emotional intensity calculation
- Consistent serialization for reproducibility

**Flow**:
```
EmotionVector → Serialize to Bytes → SHA-256 Hash → Emotion Hash (64 hex chars)
```

#### 3. Encryption Engine (`encryption_engine.py`)

**Purpose**: Performs emotion-aware AES-256 encryption.

**Key Features**:
- Two-stage key derivation (base key + emotion hash)
- AES-256-CBC encryption
- Random IV generation per encryption
- PKCS7 padding
- Complete encrypted packet creation

**Flow**:
```
Message + Secret + Emotions
    ↓
Base Key = SHA256(Secret)
    ↓
Emotion Hash = SHA256(EmotionVector)
    ↓
Final Key = SHA256(Base Key + Emotion Hash)
    ↓
Ciphertext = AES-256-CBC(Message, Final Key, Random IV)
    ↓
Encrypted Packet (Ciphertext + IV + Emotion Metadata)
```

#### 4. Decryption Module (`decryptor.py`)

**Purpose**: Reverses emotion-aware encryption and verifies emotional authenticity.

**Key Features**:
- Key reconstruction from emotion signature
- AES-256-CBC decryption
- Emotion verification via re-analysis
- Cosine similarity for emotion comparison
- Detailed verification results

**Flow**:
```
Encrypted Packet + Secret
    ↓
Reconstruct Final Key (using stored emotion signature)
    ↓
Plaintext = AES-256-CBC-Decrypt(Ciphertext, Final Key, IV)
    ↓
Re-analyze Plaintext → New EmotionVector
    ↓
Compare with Original Emotion Signature
    ↓
Decryption Result (Message + Verification Status)
```

#### 5. API Routes (`main.py`)

**Endpoints**:

1. **POST /api/encrypt**
   - Input: `{ message, user_secret }`
   - Output: `{ encrypted_packet }`
   - Process: Detect emotions → Encrypt → Return packet

2. **POST /api/decrypt**
   - Input: `{ encrypted_packet, user_secret }`
   - Output: `{ message, emotion_verified, emotions }`
   - Process: Decrypt → Verify emotions → Return result

3. **POST /api/analyze**
   - Input: `{ message }`
   - Output: `{ emotion_vector, dominant_emotions, intensity }`
   - Process: Detect emotions → Return analysis

### Data Models

#### EmotionVector
```python
{
  joy: float [0, 1],
  sadness: float [0, 1],
  anger: float [0, 1],
  fear: float [0, 1],
  surprise: float [0, 1],
  anxiety: float [0, 1]
}
```

#### EncryptedPacket
```python
{
  encrypted_text: str (base64),
  iv: str (base64),
  emotion_signature: EmotionVector,
  dominant_emotions: List[str],
  emotional_intensity: float [0, 1]
}
```

#### DecryptionResult
```python
{
  message: str,
  emotion_verified: bool,
  original_emotions: EmotionVector,
  detected_emotions: EmotionVector,
  verification_threshold: float
}
```

## Frontend Architecture

### Component Structure

```
app/
├── layout.tsx          # Root layout with global styles
├── page.tsx            # Main application page with state management
└── globals.css         # Global styles + glassmorphism utilities

components/
├── MessageInput.tsx              # Message input form
├── EmotionAnalysisScreen.tsx    # Loading screen during analysis
├── EncryptionResultScreen.tsx   # Display encrypted result
├── DecryptionInput.tsx          # Decryption input form
├── DecryptionResultScreen.tsx   # Display decrypted result
├── EmotionBars.tsx              # Emotion intensity bars
├── RadarChart.tsx               # Emotion radar chart
└── EmotionAura.tsx              # Animated emotion aura

lib/
├── types.ts            # TypeScript type definitions
└── api.ts              # API client functions
```

### State Management

The application uses React's built-in state management:

- **Local State**: Component-specific state (form inputs, loading states)
- **Lifted State**: Shared state in `page.tsx` (current screen, emotion data, encrypted packets)
- **No Redux/Context**: Simple enough for prop drilling

### UI Design System

#### Glassmorphism

All UI components use a consistent glassmorphism design:

```css
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  border-radius: 16px;
}
```

#### Color Palette

**Emotion Colors**:
- Joy: `#FFD700` (Yellow)
- Sadness: `#4169E1` (Blue)
- Anger: `#DC143C` (Red)
- Fear: `#9370DB` (Purple)
- Surprise: `#32CD32` (Green)
- Anxiety: `#FF8C00` (Orange)

**Background Gradient**:
```css
linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)
```

### Animation Strategy

All animations use **Framer Motion** for smooth, performant transitions:

1. **Screen Transitions**: Fade + slide animations
2. **Emotion Bars**: Staggered width animations
3. **Emotion Aura**: Pulsing scale + opacity
4. **Loading States**: Rotating icons + bouncing dots

## Security Considerations

### Encryption

- **Algorithm**: AES-256-CBC (industry standard)
- **Key Derivation**: SHA-256 (cryptographically secure)
- **IV**: Random 16 bytes per encryption (prevents pattern analysis)
- **Padding**: PKCS7 (standard padding scheme)

### Emotion-Aware Key Derivation

The emotion hash is **publicly visible** in the encrypted packet. This is intentional:

1. Allows emotional analysis without decryption
2. Enables emotion verification after decryption
3. Does not compromise message security (emotion hash alone cannot decrypt)

**Security Property**: Even if an attacker knows the emotion signature, they still need the user secret to derive the final encryption key.

### Threat Model

**Protected Against**:
- Unauthorized message access (requires secret key)
- Ciphertext pattern analysis (random IV per encryption)
- Emotion tampering (verification detects changes)

**Not Protected Against**:
- Weak user secrets (users must choose strong keys)
- Side-channel attacks (not in scope for this application)
- Quantum computing (AES-256 is quantum-resistant for now)

## Performance Optimizations

### Backend

1. **Model Caching**: HuggingFace model loaded once at startup
2. **GPU Acceleration**: Automatic GPU detection and usage
3. **Warmup Inference**: Test inference on startup to load model into memory
4. **Async Endpoints**: FastAPI async handlers for concurrent requests

### Frontend

1. **Code Splitting**: Next.js automatic code splitting
2. **Lazy Loading**: Components loaded on demand
3. **Memoization**: React useMemo for expensive calculations
4. **Optimized Animations**: GPU-accelerated CSS transforms

## Testing Strategy

### Backend Tests

**Unit Tests** (`tests/unit/`):
- Individual component testing
- Edge case validation
- Error handling verification

**Integration Tests** (`tests/integration/`):
- Full encryption/decryption flow
- API endpoint testing
- Cross-component interactions

**Property-Based Tests** (optional):
- Hypothesis library for randomized testing
- Universal property verification
- Fuzz testing for edge cases

### Frontend Tests

**Unit Tests**:
- Component rendering
- User interactions
- API client functions

**Integration Tests**:
- Full user flows
- Screen transitions
- Error handling

### Test Coverage Goals

- Backend: 85%+ code coverage
- Frontend: 75%+ code coverage
- Critical paths: 100% coverage

## Deployment Considerations

### Backend Deployment

**Requirements**:
- Python 3.10+
- 2GB RAM minimum (for model)
- GPU optional (improves performance)

**Recommended Platforms**:
- AWS EC2 (with GPU instance for production)
- Google Cloud Run (CPU-only, slower)
- Heroku (with performance dynos)

### Frontend Deployment

**Requirements**:
- Node.js 18+
- Static hosting or serverless

**Recommended Platforms**:
- Vercel (optimal for Next.js)
- Netlify
- AWS Amplify

### Environment Variables

**Backend**:
```bash
# Optional
CUDA_VISIBLE_DEVICES=0  # GPU selection
MODEL_CACHE_DIR=./models  # Model cache location
```

**Frontend**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
```

## Scalability

### Current Limitations

- Single-instance backend (no load balancing)
- Model loaded in memory (not shared across instances)
- No caching layer for repeated analyses

### Scaling Strategies

1. **Horizontal Scaling**: Deploy multiple backend instances behind load balancer
2. **Model Serving**: Use dedicated model serving infrastructure (TensorFlow Serving, TorchServe)
3. **Caching**: Add Redis for emotion analysis caching
4. **Database**: Add PostgreSQL for storing encrypted packets (optional)

## Future Enhancements

### Potential Features

1. **Multi-language Support**: Extend emotion detection to other languages
2. **Emotion Dashboard**: Aggregate emotional analytics over time
3. **Batch Processing**: Encrypt/decrypt multiple messages at once
4. **Custom Models**: Allow users to bring their own emotion detection models
5. **Blockchain Integration**: Store emotion signatures on-chain for immutability

### Technical Improvements

1. **WebAssembly**: Run emotion detection in browser (privacy + performance)
2. **Progressive Web App**: Offline support with service workers
3. **Real-time Collaboration**: WebSocket support for live emotion sharing
4. **Mobile Apps**: React Native versions for iOS/Android

---

**Built with ❤️ for hackathons** 🏆

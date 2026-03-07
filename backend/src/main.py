"""FastAPI application for EMOTION CIPHER"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from typing import Dict, List, Optional
from dataclasses import asdict
import logging

from .emotion_detector import EmotionDetector, EmotionDetectionError
from .emotion_encoder import EmotionEncoder
from .encryption_engine import EncryptionEngine
from .decryptor import DecryptionModule, DecryptionError
from .models import EncryptedPacket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
emotion_detector: Optional[EmotionDetector] = None
emotion_encoder: Optional[EmotionEncoder] = None
encryption_engine: Optional[EncryptionEngine] = None
decryption_module: Optional[DecryptionModule] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize models on startup"""
    global emotion_detector, emotion_encoder, encryption_engine, decryption_module
    
    logger.info("Loading emotion detection model...")
    try:
        emotion_detector = EmotionDetector()
        emotion_encoder = EmotionEncoder()
        encryption_engine = EncryptionEngine(emotion_encoder)
        decryption_module = DecryptionModule(emotion_detector, emotion_encoder)
        
        # Warmup inference
        logger.info("Warming up model...")
        emotion_detector.detect_emotions("This is a test message.")
        logger.info("Model loaded and ready!")
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise
    
    yield
    
    # Cleanup
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="EMOTION CIPHER API",
    description="Emotion-aware encryption API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:4000",
        "http://127.0.0.1:4000",
        "https://*.vercel.app",  # Allow all Vercel deployments
        "https://vercel.app",
        # Add your specific Vercel domain here:
        # "https://your-app-name.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class EncryptRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    user_secret: str = Field(..., min_length=1)


class EncryptResponse(BaseModel):
    encrypted_packet: Dict


class DecryptRequest(BaseModel):
    encrypted_packet: Dict
    user_secret: str = Field(..., min_length=1)


class DecryptResponse(BaseModel):
    message: str
    emotion_verified: bool
    original_emotions: Dict[str, float]
    detected_emotions: Dict[str, float]


class AnalyzeRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)


class AnalyzeResponse(BaseModel):
    emotion_vector: Dict[str, float]
    dominant_emotions: List[str]
    emotional_intensity: float


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "EMOTION CIPHER API",
        "version": "1.0.0"
    }


@app.post("/api/encrypt", response_model=EncryptResponse)
async def encrypt_message(request: EncryptRequest):
    """
    Encrypt message with emotion-aware encryption
    
    The encryption key is derived from both the user secret and
    the emotional signature of the message, ensuring that identical
    messages with different emotions produce different ciphertexts.
    """
    try:
        # Detect emotions
        emotion_vector = emotion_detector.detect_emotions(request.message)
        
        # Encrypt with emotion-aware key derivation
        encrypted_packet = encryption_engine.encrypt(
            request.message,
            request.user_secret,
            emotion_vector
        )
        
        return EncryptResponse(
            encrypted_packet=asdict(encrypted_packet)
        )
        
    except EmotionDetectionError as e:
        raise HTTPException(status_code=500, detail=f"Emotion detection failed: {str(e)}")
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")


@app.post("/api/decrypt", response_model=DecryptResponse)
async def decrypt_message(request: DecryptRequest):
    """
    Decrypt message and verify emotion signature
    
    Reconstructs the encryption key using the emotion signature
    from the encrypted packet, then verifies that the decrypted
    message's emotions match the original signature.
    """
    try:
        # Parse encrypted packet
        packet = EncryptedPacket(**request.encrypted_packet)
        
        # Decrypt and verify
        result = decryption_module.decrypt(packet, request.user_secret)
        
        return DecryptResponse(
            message=result.message,
            emotion_verified=result.emotion_verified,
            original_emotions=result.original_emotions,
            detected_emotions=result.detected_emotions
        )
        
    except DecryptionError as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_emotion(request: AnalyzeRequest):
    """
    Analyze emotion without encryption
    
    Useful for previewing emotional content before encryption
    or for standalone emotion analysis.
    """
    try:
        # Detect emotions
        emotion_vector = emotion_detector.detect_emotions(request.message)
        
        # Extract metadata
        dominant_emotions = emotion_encoder.extract_dominant_emotions(emotion_vector)
        emotional_intensity = emotion_encoder.calculate_intensity(emotion_vector)
        
        return AnalyzeResponse(
            emotion_vector=emotion_vector.to_dict(),
            dominant_emotions=dominant_emotions,
            emotional_intensity=emotional_intensity
        )
        
    except EmotionDetectionError as e:
        raise HTTPException(status_code=500, detail=f"Emotion detection failed: {str(e)}")
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

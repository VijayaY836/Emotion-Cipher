"""Data models for EMOTION CIPHER"""
from dataclasses import dataclass, asdict
from typing import List, Dict
import json
import struct


@dataclass
class EmotionVector:
    """Normalized emotion scores in [0, 1] range"""
    joy: float
    sadness: float
    anger: float
    fear: float
    surprise: float
    anxiety: float
    excitement: float
    
    def __post_init__(self):
        """Validate emotion scores are in [0, 1] range"""
        for emotion in ['joy', 'sadness', 'anger', 'fear', 'surprise', 'anxiety', 'excitement']:
            value = getattr(self, emotion)
            if not 0 <= value <= 1:
                raise ValueError(f"{emotion} must be in [0, 1] range, got {value}")
    
    def to_dict(self) -> Dict[str, float]:
        """Serialize to dictionary"""
        return asdict(self)
    
    def to_bytes(self) -> bytes:
        """Serialize to bytes for hashing (deterministic)"""
        # Use consistent ordering and precision
        emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'anxiety', 'excitement']
        return b''.join(struct.pack('d', getattr(self, e)) for e in emotions)


@dataclass
class EncryptedPacket:
    """Complete encrypted message with emotion metadata"""
    encrypted_text: str  # Base64-encoded ciphertext
    iv: str  # Base64-encoded initialization vector
    emotion_signature: Dict[str, float]  # Public emotion metadata
    dominant_emotions: List[str]  # Sorted by intensity
    emotional_intensity: float  # Overall intensity [0, 1]
    
    def to_json(self) -> str:
        """Serialize to JSON string"""
        return json.dumps(asdict(self), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'EncryptedPacket':
        """Deserialize from JSON string"""
        data = json.loads(json_str)
        return cls(**data)


@dataclass
class DecryptionResult:
    """Result of decryption with emotion verification"""
    message: str
    emotion_verified: bool
    original_emotions: Dict[str, float]
    detected_emotions: Dict[str, float]
    verification_threshold: float = 0.15  # Cosine distance threshold

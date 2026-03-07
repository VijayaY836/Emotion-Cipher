"""Unit tests for data models"""
import pytest
import json
from src.models import EmotionVector, EncryptedPacket, DecryptionResult


def test_emotion_vector_validation():
    """Test EmotionVector validates range [0, 1]"""
    # Valid emotion vector
    emotion = EmotionVector(joy=0.5, sadness=0.3, anger=0.1, fear=0.05, surprise=0.03, anxiety=0.02)
    assert emotion.joy == 0.5
    
    # Invalid emotion vector (out of range)
    with pytest.raises(ValueError):
        EmotionVector(joy=1.5, sadness=0.3, anger=0.1, fear=0.05, surprise=0.03, anxiety=0.02)
    
    with pytest.raises(ValueError):
        EmotionVector(joy=-0.1, sadness=0.3, anger=0.1, fear=0.05, surprise=0.03, anxiety=0.02)


def test_emotion_vector_to_dict():
    """Test EmotionVector serialization to dict"""
    emotion = EmotionVector(joy=0.8, sadness=0.1, anger=0.05, fear=0.02, surprise=0.02, anxiety=0.01)
    emotion_dict = emotion.to_dict()
    
    assert isinstance(emotion_dict, dict)
    assert emotion_dict['joy'] == 0.8
    assert emotion_dict['sadness'] == 0.1
    assert len(emotion_dict) == 6


def test_emotion_vector_to_bytes():
    """Test EmotionVector serialization to bytes"""
    emotion = EmotionVector(joy=0.8, sadness=0.1, anger=0.05, fear=0.02, surprise=0.02, anxiety=0.01)
    emotion_bytes = emotion.to_bytes()
    
    assert isinstance(emotion_bytes, bytes)
    assert len(emotion_bytes) == 48  # 6 emotions * 8 bytes per double


def test_encrypted_packet_serialization():
    """Test EncryptedPacket JSON serialization"""
    emotion = EmotionVector(joy=0.8, sadness=0.1, anger=0.05, fear=0.02, surprise=0.02, anxiety=0.01)
    packet = EncryptedPacket(
        encrypted_text="base64encodedtext",
        iv="base64encodediv",
        emotion_signature=emotion.to_dict(),
        dominant_emotions=['joy'],
        emotional_intensity=0.8
    )
    
    # Serialize to JSON
    json_str = packet.to_json()
    assert isinstance(json_str, str)
    
    # Deserialize from JSON
    parsed = EncryptedPacket.from_json(json_str)
    assert parsed.encrypted_text == packet.encrypted_text
    assert parsed.iv == packet.iv
    assert parsed.dominant_emotions == packet.dominant_emotions


def test_decryption_result_structure():
    """Test DecryptionResult structure"""
    result = DecryptionResult(
        message="Hello, world!",
        emotion_verified=True,
        original_emotions={'joy': 0.8, 'sadness': 0.1, 'anger': 0.05, 'fear': 0.02, 'surprise': 0.02, 'anxiety': 0.01},
        detected_emotions={'joy': 0.75, 'sadness': 0.12, 'anger': 0.05, 'fear': 0.03, 'surprise': 0.03, 'anxiety': 0.02}
    )
    
    assert result.message == "Hello, world!"
    assert result.emotion_verified is True
    assert result.verification_threshold == 0.15

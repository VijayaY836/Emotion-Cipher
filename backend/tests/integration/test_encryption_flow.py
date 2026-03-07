"""Integration tests for full encryption/decryption flow"""
import pytest
from src.emotion_detector import EmotionDetector
from src.emotion_encoder import EmotionEncoder
from src.encryption_engine import EncryptionEngine
from src.decryptor import DecryptionModule


@pytest.fixture
def emotion_detector():
    return EmotionDetector()


@pytest.fixture
def emotion_encoder():
    return EmotionEncoder()


@pytest.fixture
def encryption_engine(emotion_encoder):
    return EncryptionEngine(emotion_encoder)


@pytest.fixture
def decryption_module(emotion_detector, emotion_encoder):
    return DecryptionModule(emotion_detector, emotion_encoder)


def test_full_encryption_decryption_flow(
    emotion_detector, 
    encryption_engine, 
    decryption_module
):
    """Test complete encryption and decryption flow"""
    # Original message
    message = "I am so happy today! This is wonderful!"
    secret = "my_secret_key_123"
    
    # Detect emotions
    emotions = emotion_detector.detect_emotions(message)
    assert emotions.joy > 0  # Should detect happiness
    
    # Encrypt
    encrypted_packet = encryption_engine.encrypt(message, secret, emotions)
    assert encrypted_packet.encrypted_text
    assert encrypted_packet.iv
    assert len(encrypted_packet.dominant_emotions) > 0
    
    # Decrypt
    result = decryption_module.decrypt(encrypted_packet, secret)
    assert result.message == message
    assert result.emotion_verified  # Emotions should match


def test_wrong_key_fails_decryption(
    emotion_detector,
    encryption_engine,
    decryption_module
):
    """Test that wrong key fails decryption"""
    message = "Secret message"
    correct_secret = "correct_key"
    wrong_secret = "wrong_key"
    
    # Encrypt with correct key
    emotions = emotion_detector.detect_emotions(message)
    encrypted_packet = encryption_engine.encrypt(message, correct_secret, emotions)
    
    # Try to decrypt with wrong key
    with pytest.raises(Exception):  # Should raise decryption error
        decryption_module.decrypt(encrypted_packet, wrong_secret)


def test_different_emotions_different_ciphertext(
    emotion_detector,
    encryption_engine
):
    """Test that same message with different emotions produces different ciphertext"""
    message = "This is a test message"
    secret = "my_secret"
    
    # Create two different emotion vectors
    from src.models import EmotionVector
    emotion1 = EmotionVector(joy=0.8, sadness=0.1, anger=0.05, fear=0.02, surprise=0.02, anxiety=0.01)
    emotion2 = EmotionVector(joy=0.1, sadness=0.8, anger=0.05, fear=0.02, surprise=0.02, anxiety=0.01)
    
    # Encrypt same message with different emotions
    packet1 = encryption_engine.encrypt(message, secret, emotion1)
    packet2 = encryption_engine.encrypt(message, secret, emotion2)
    
    # Ciphertexts should be different
    assert packet1.encrypted_text != packet2.encrypted_text

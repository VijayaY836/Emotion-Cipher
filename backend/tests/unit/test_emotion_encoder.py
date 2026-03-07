"""Unit tests for EmotionEncoder"""
import pytest
from src.emotion_encoder import EmotionEncoder
from src.models import EmotionVector


@pytest.fixture
def encoder():
    return EmotionEncoder()


@pytest.fixture
def sample_emotion():
    return EmotionVector(
        joy=0.8, sadness=0.1, anger=0.05,
        fear=0.02, surprise=0.02, anxiety=0.01
    )


def test_encode_emotion_hash_deterministic(encoder, sample_emotion):
    """Test that same emotion vector produces same hash"""
    hash1 = encoder.encode_emotion_hash(sample_emotion)
    hash2 = encoder.encode_emotion_hash(sample_emotion)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 produces 64 hex characters


def test_encode_emotion_hash_unique(encoder):
    """Test that different emotions produce different hashes"""
    emotion1 = EmotionVector(joy=0.8, sadness=0.1, anger=0.05, fear=0.02, surprise=0.02, anxiety=0.01)
    emotion2 = EmotionVector(joy=0.1, sadness=0.8, anger=0.05, fear=0.02, surprise=0.02, anxiety=0.01)
    
    hash1 = encoder.encode_emotion_hash(emotion1)
    hash2 = encoder.encode_emotion_hash(emotion2)
    
    assert hash1 != hash2


def test_extract_dominant_emotions(encoder, sample_emotion):
    """Test dominant emotion extraction with threshold"""
    dominant = encoder.extract_dominant_emotions(sample_emotion, threshold=0.3)
    
    assert 'joy' in dominant
    assert 'sadness' not in dominant  # Below threshold
    assert dominant[0] == 'joy'  # Highest intensity first


def test_extract_dominant_emotions_sorted(encoder):
    """Test that dominant emotions are sorted by intensity"""
    emotion = EmotionVector(joy=0.5, sadness=0.7, anger=0.3, fear=0.1, surprise=0.1, anxiety=0.1)
    dominant = encoder.extract_dominant_emotions(emotion, threshold=0.25)
    
    assert dominant == ['sadness', 'joy', 'anger']


def test_calculate_intensity(encoder, sample_emotion):
    """Test emotional intensity calculation"""
    intensity = encoder.calculate_intensity(sample_emotion)
    
    assert 0 <= intensity <= 1
    assert intensity == 0.8  # Max emotion is joy at 0.8


def test_calculate_intensity_neutral(encoder):
    """Test intensity for neutral emotions"""
    neutral = EmotionVector(joy=0.0, sadness=0.0, anger=0.0, fear=0.0, surprise=0.0, anxiety=0.0)
    intensity = encoder.calculate_intensity(neutral)
    
    assert intensity == 0.0

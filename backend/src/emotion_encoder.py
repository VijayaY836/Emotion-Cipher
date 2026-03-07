"""Emotion signature encoding and hashing"""
import hashlib
from typing import List, Tuple
from .models import EmotionVector


class EmotionEncoder:
    """Transforms emotion vectors into cryptographic signatures"""
    
    def encode_emotion_hash(self, emotion_vector: EmotionVector) -> str:
        """
        Create SHA-256 hash from emotion vector
        
        Args:
            emotion_vector: Normalized emotion scores
            
        Returns:
            Hexadecimal emotion hash string
        """
        # Serialize emotion vector deterministically
        emotion_bytes = emotion_vector.to_bytes()
        
        # Compute SHA-256 hash
        hash_obj = hashlib.sha256(emotion_bytes)
        return hash_obj.hexdigest()
    
    def extract_dominant_emotions(
        self, 
        emotion_vector: EmotionVector, 
        threshold: float = 0.10,  # Lowered to 10% to catch more emotions
        max_emotions: int = 3      # Show top 3 emotions
    ) -> List[str]:
        """
        Identify dominant emotions
        
        Args:
            emotion_vector: Emotion scores
            threshold: Minimum intensity to be considered (default 10%)
            max_emotions: Maximum number of emotions to return
            
        Returns:
            List of emotion names sorted by intensity (descending)
        """
        emotions = emotion_vector.to_dict()
        
        # Get all emotions sorted by intensity
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        
        # Take top emotions above threshold, up to max_emotions
        dominant = []
        for name, score in sorted_emotions:
            if score >= threshold and len(dominant) < max_emotions:
                dominant.append(name)
        
        # If no emotions above threshold, return top emotion
        if not dominant and sorted_emotions:
            dominant.append(sorted_emotions[0][0])
        
        return dominant
    
    def calculate_intensity(self, emotion_vector: EmotionVector) -> float:
        """
        Calculate overall emotional intensity
        
        Returns:
            Intensity score in [0, 1] range
        """
        emotions = emotion_vector.to_dict()
        
        # Use max emotion as intensity (alternative: could use sum or mean)
        # Max gives us the strength of the dominant emotion
        return max(emotions.values())

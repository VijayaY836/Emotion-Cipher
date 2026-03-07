"""Emotion-aware AES-256 encryption"""
import hashlib
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from .models import EmotionVector, EncryptedPacket
from .emotion_encoder import EmotionEncoder


class EncryptionEngine:
    """Performs emotion-aware AES-256 encryption"""
    
    def __init__(self, emotion_encoder: EmotionEncoder):
        """Initialize with emotion encoder"""
        self.emotion_encoder = emotion_encoder
    
    def encrypt(
        self, 
        message: str, 
        user_secret: str, 
        emotion_vector: EmotionVector
    ) -> EncryptedPacket:
        """
        Encrypt message with emotion-aware key derivation
        
        Args:
            message: Plaintext message
            user_secret: User's encryption secret
            emotion_vector: Detected emotions
            
        Returns:
            EncryptedPacket with ciphertext and emotion metadata
        """
        # Derive base key from user secret
        base_key = self._derive_base_key(user_secret)
        
        # Compute emotion hash
        emotion_hash = self.emotion_encoder.encode_emotion_hash(emotion_vector)
        
        # Derive final key combining base key and emotion hash
        final_key = self._derive_final_key(base_key, emotion_hash)
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Encrypt message
        ciphertext = self._aes_encrypt(message, final_key, iv)
        
        # Extract emotion metadata
        dominant_emotions = self.emotion_encoder.extract_dominant_emotions(emotion_vector)
        emotional_intensity = self.emotion_encoder.calculate_intensity(emotion_vector)
        
        # Create encrypted packet
        return EncryptedPacket(
            encrypted_text=base64.b64encode(ciphertext).decode('utf-8'),
            iv=base64.b64encode(iv).decode('utf-8'),
            emotion_signature=emotion_vector.to_dict(),
            dominant_emotions=dominant_emotions,
            emotional_intensity=emotional_intensity
        )
    
    def _derive_base_key(self, user_secret: str) -> bytes:
        """Derive base key from user secret using SHA-256"""
        return hashlib.sha256(user_secret.encode('utf-8')).digest()
    
    def _derive_final_key(self, base_key: bytes, emotion_hash: str) -> bytes:
        """Combine base key with emotion hash to create final key"""
        # Concatenate base key and emotion hash, then hash again
        combined = base_key + emotion_hash.encode('utf-8')
        return hashlib.sha256(combined).digest()
    
    def _aes_encrypt(self, plaintext: str, key: bytes, iv: bytes) -> bytes:
        """Perform AES-256-CBC encryption with PKCS7 padding"""
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
        return cipher.encrypt(padded_data)

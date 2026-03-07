"""Emotion-aware decryption and verification"""
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from .models import EncryptedPacket, DecryptionResult, EmotionVector
from .emotion_detector import EmotionDetector
from .emotion_encoder import EmotionEncoder
import math


class DecryptionError(Exception):
    """Raised when decryption fails"""
    pass


class DecryptionModule:
    """Reverses emotion-aware encryption and verifies emotional authenticity"""
    
    def __init__(self, emotion_detector: EmotionDetector, emotion_encoder: EmotionEncoder):
        """Initialize with emotion detector for verification"""
        self.emotion_detector = emotion_detector
        self.emotion_encoder = emotion_encoder
    
    def decrypt(
        self, 
        encrypted_packet: EncryptedPacket, 
        user_secret: str
    ) -> DecryptionResult:
        """
        Decrypt message and verify emotion signature
        
        Args:
            encrypted_packet: Encrypted data with emotion metadata
            user_secret: User's decryption secret
            
        Returns:
            DecryptionResult with plaintext and verification status
            
        Raises:
            DecryptionError: If decryption fails
        """
        try:
            # Reconstruct emotion vector from signature
            emotion_vector = EmotionVector(**encrypted_packet.emotion_signature)
            
            # Derive base key from user secret
            base_key = self._derive_base_key(user_secret)
            
            # Compute emotion hash from signature
            emotion_hash = self.emotion_encoder.encode_emotion_hash(emotion_vector)
            
            # Derive final key
            final_key = self._derive_final_key(base_key, emotion_hash)
            
            # Decode base64 data
            ciphertext = base64.b64decode(encrypted_packet.encrypted_text)
            iv = base64.b64decode(encrypted_packet.iv)
            
            # Decrypt
            plaintext = self._aes_decrypt(ciphertext, final_key, iv)
            
            # Verify emotion signature
            detected_emotions = self.emotion_detector.detect_emotions(plaintext)
            emotion_verified = self._verify_emotion_signature(
                emotion_vector, 
                detected_emotions
            )
            
            return DecryptionResult(
                message=plaintext,
                emotion_verified=emotion_verified,
                original_emotions=encrypted_packet.emotion_signature,
                detected_emotions=detected_emotions.to_dict()
            )
            
        except Exception as e:
            raise DecryptionError(f"Decryption failed: {str(e)}")
    
    def _derive_base_key(self, user_secret: str) -> bytes:
        """Derive base key from user secret using SHA-256"""
        return hashlib.sha256(user_secret.encode('utf-8')).digest()
    
    def _derive_final_key(self, base_key: bytes, emotion_hash: str) -> bytes:
        """Combine base key with emotion hash to create final key"""
        combined = base_key + emotion_hash.encode('utf-8')
        return hashlib.sha256(combined).digest()
    
    def _aes_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> str:
        """Perform AES-256-CBC decryption"""
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        return plaintext.decode('utf-8')
    
    def _verify_emotion_signature(
        self, 
        original: EmotionVector, 
        detected: EmotionVector
    ) -> bool:
        """
        Re-analyze message and compare with original emotion signature
        
        Uses cosine similarity to compare emotion vectors.
        Returns True if vectors are similar within threshold.
        """
        orig_dict = original.to_dict()
        det_dict = detected.to_dict()
        
        # Calculate cosine similarity
        dot_product = sum(orig_dict[k] * det_dict[k] for k in orig_dict.keys())
        
        orig_magnitude = math.sqrt(sum(v ** 2 for v in orig_dict.values()))
        det_magnitude = math.sqrt(sum(v ** 2 for v in det_dict.values()))
        
        if orig_magnitude == 0 or det_magnitude == 0:
            # Both neutral or one is neutral
            return orig_magnitude == det_magnitude
        
        cosine_similarity = dot_product / (orig_magnitude * det_magnitude)
        
        # Cosine distance = 1 - similarity
        # Threshold of 0.15 means vectors should be quite similar
        cosine_distance = 1 - cosine_similarity
        
        return cosine_distance < 0.15

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

from emotion_detector import EmotionDetector
from emotion_encoder import EmotionEncoder
from encryption_engine import EncryptionEngine
from models import EncryptRequest, EncryptedPacket

# Initialize components
detector = EmotionDetector()
encoder = EmotionEncoder()
engine = EncryptionEngine()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            # Process request
            request = EncryptRequest(**data)
            
            # Detect emotions
            emotions = detector.detect_emotions(request.message)
            
            # Generate emotion hash
            emotion_hash = encoder.encode_emotions(emotions)
            
            # Encrypt message
            encrypted_packet = engine.encrypt(
                message=request.message,
                user_secret=request.user_secret,
                emotion_hash=emotion_hash,
                emotions=emotions
            )
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'encrypted_packet': encrypted_packet.dict()
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'detail': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

"""Emotion detection using HuggingFace transformers"""
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from functools import lru_cache
from typing import Optional
from .models import EmotionVector


class EmotionDetectionError(Exception):
    """Raised when emotion detection fails"""
    pass


class EmotionDetector:
    """Analyzes text and extracts emotional content"""
    
    MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
    # Correct label order from model config: {0: 'anger', 1: 'disgust', 2: 'fear', 3: 'joy', 4: 'neutral', 5: 'sadness', 6: 'surprise'}
    EMOTION_LABELS = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
    
    def __init__(self):
        """Load emotion detection model"""
        self.model, self.tokenizer = self._load_model()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.eval()
    
    @lru_cache(maxsize=1)
    def _load_model(self):
        """Load and cache HuggingFace model with memory optimization"""
        try:
            model = AutoModelForSequenceClassification.from_pretrained(
                self.MODEL_NAME,
                cache_dir="./models",
                torch_dtype=torch.float16,  # Use half precision - saves 50% memory
                low_cpu_mem_usage=True      # Optimize CPU memory usage
            )
            tokenizer = AutoTokenizer.from_pretrained(
                self.MODEL_NAME,
                cache_dir="./models"
            )
            return model, tokenizer
        except Exception as e:
            raise EmotionDetectionError(f"Failed to load model: {str(e)}")
    
    def detect_emotions(self, text: str) -> EmotionVector:
        """
        Analyze text and return emotion scores
        
        Args:
            text: Input message to analyze
            
        Returns:
            EmotionVector with normalized scores for six emotions
            
        Raises:
            EmotionDetectionError: If analysis fails
        """
        # Handle empty/whitespace input
        if not text or text.strip() == "":
            return EmotionVector(
                joy=0.0, sadness=0.0, anger=0.0,
                fear=0.0, surprise=0.0, anxiety=0.0, excitement=0.0
            )
        
        try:
            # Tokenize and run inference
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
                scores = scores.cpu().numpy()[0]
            
            # Map model outputs to our emotion structure
            raw_emotions = dict(zip(self.EMOTION_LABELS, scores))
            
            # Normalize and structure
            normalized = self._normalize_scores(raw_emotions)
            
            return EmotionVector(
                joy=normalized['joy'],
                sadness=normalized['sadness'],
                anger=normalized['anger'],
                fear=normalized['fear'],
                surprise=normalized['surprise'],
                anxiety=normalized['anxiety'],
                excitement=normalized['excitement']
            )
            
        except Exception as e:
            raise EmotionDetectionError(f"Emotion detection failed: {str(e)}")
    
    def _normalize_scores(self, raw_scores: dict) -> dict:
        """
        Normalize emotion scores and map to our 7-emotion structure
        
        Model outputs: anger, disgust, fear, joy, neutral, sadness, surprise
        We want: joy, sadness, anger, fear, surprise, anxiety, excitement
        
        Key insight: Excitement = Joy + Surprise (high arousal positive emotion)
        """
        fear_score = raw_scores.get('fear', 0.0)
        neutral_score = raw_scores.get('neutral', 0.0)
        joy_score = raw_scores.get('joy', 0.0)
        surprise_score = raw_scores.get('surprise', 0.0)
        
        # Calculate excitement: when joy and surprise co-occur, it's excitement
        # Excitement is high-arousal joy (thrilled, excited, exhilarated)
        excitement_score = 0.0
        if joy_score > 0.5:
            if surprise_score > 0.02:
                # Strong joy + some surprise = excitement
                excitement_score = min(joy_score * 0.6, surprise_score * 12)
                joy_score = joy_score * 0.55
                surprise_score = surprise_score * 0.25
            elif surprise_score > 0.01:
                # Even minimal surprise with strong joy can be excitement
                excitement_score = joy_score * 0.25
                joy_score = joy_score * 0.65
        
        # Split fear into fear and anxiety, and boost anxiety detection
        anxiety_from_fear = fear_score * 0.8  # Increased from 0.7
        pure_fear = fear_score * 0.2          # Decreased from 0.3
        
        # Boost anxiety from neutral more
        anxiety_base = anxiety_from_fear + (neutral_score * 1.5)
        
        normalized = {
            'joy': joy_score,
            'sadness': raw_scores.get('sadness', 0.0),
            'anger': raw_scores.get('anger', 0.0) + raw_scores.get('disgust', 0.0),
            'fear': pure_fear,
            'surprise': surprise_score,
            'anxiety': anxiety_base,
            'excitement': excitement_score
        }
        
        # Apply rebalancing
        normalized = self._rebalance_emotions(normalized)
        
        # Ensure all values are in [0, 1]
        for key in normalized:
            normalized[key] = max(0.0, min(1.0, float(normalized[key])))
        
        return normalized
    
    def _rebalance_emotions(self, emotions: dict) -> dict:
        """
        Rebalance emotion distribution to be less extreme
        
        The softmax output from the model is often too concentrated (95%+ on one emotion).
        This function redistributes probabilities to make mixed emotions more visible.
        Also applies contextual filtering to remove inappropriate emotions.
        """
        # Contextual filtering: Remove surprise when it conflicts with context
        # "I can't believe" triggers surprise, but with sadness/anger it's disbelief, not surprise
        if emotions.get('surprise', 0) > 0.05:
            negative_emotions = emotions.get('sadness', 0) + emotions.get('anger', 0) + emotions.get('fear', 0)
            # If strong negative emotions (>40%) and surprise is present, it's likely disbelief
            if negative_emotions > 0.40:
                # Redistribute surprise to the dominant negative emotion
                surprise_amount = emotions['surprise']
                if emotions.get('sadness', 0) > emotions.get('anger', 0):
                    emotions['sadness'] += surprise_amount * 0.5
                else:
                    emotions['anger'] += surprise_amount * 0.5
                emotions['surprise'] = surprise_amount * 0.1  # Keep minimal surprise
        
        # Protect anxiety from being suppressed - boost it if it's present
        anxiety_boost = 1.0
        if emotions.get('anxiety', 0) > 0.015:  # If anxiety is >1.5%
            anxiety_boost = 8.0  # Significantly boost anxiety visibility
            emotions['anxiety'] = emotions['anxiety'] * anxiety_boost
        
        # Sort emotions by score
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        
        # If the top emotion is overwhelming (>80%), redistribute some to secondary emotions
        if sorted_emotions[0][1] > 0.80:
            dominant_name, dominant_score = sorted_emotions[0]
            
            # Calculate how much to redistribute
            excess = dominant_score - 0.60  # Bring dominant down to 60%
            
            # Find secondary emotions (those with >1% score), prioritize anxiety
            secondary = [(name, score) for name, score in sorted_emotions[1:] if score > 0.01]
            
            if secondary:
                # Distribute excess proportionally to secondary emotions
                total_secondary = sum(score for _, score in secondary)
                
                # Boost secondary emotions
                for name, score in secondary:
                    if total_secondary > 0:
                        multiplier = 3.0 if name == 'anxiety' else 2.5  # Extra boost for anxiety
                        boost = excess * (score / total_secondary) * multiplier
                        emotions[name] = score + boost
                
                # Reduce dominant emotion
                emotions[dominant_name] = 0.60
        
        # Renormalize to sum to 1.0
        total = sum(emotions.values())
        if total > 0:
            for key in emotions:
                emotions[key] = emotions[key] / total
        
        return emotions

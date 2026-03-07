/**
 * TypeScript types for EMOTION CIPHER
 */

export interface EmotionVector {
  joy: number;
  sadness: number;
  anger: number;
  fear: number;
  surprise: number;
  anxiety: number;
  excitement: number;
}

export interface EncryptedPacket {
  encrypted_text: string;
  iv: string;
  emotion_signature: EmotionVector;
  dominant_emotions: string[];
  emotional_intensity: number;
}

export interface DecryptionResult {
  message: string;
  emotion_verified: boolean;
  original_emotions: EmotionVector;
  detected_emotions: EmotionVector;
}

export interface AnalyzeResponse {
  emotion_vector: EmotionVector;
  dominant_emotions: string[];
  emotional_intensity: number;
}

export const EMOTION_COLORS: Record<string, string> = {
  joy: '#FFD700',      // Yellow
  sadness: '#4169E1',  // Blue
  anger: '#DC143C',    // Red
  fear: '#9370DB',     // Purple
  surprise: '#32CD32', // Green
  anxiety: '#FF8C00',  // Orange
  excitement: '#FF1493' // Deep Pink (vibrant, energetic)
};

export const EMOTION_LABELS: Record<string, string> = {
  joy: 'Joy',
  sadness: 'Sadness',
  anger: 'Anger',
  fear: 'Fear',
  surprise: 'Surprise',
  anxiety: 'Anxiety',
  excitement: 'Excitement'
};

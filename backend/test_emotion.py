from src.emotion_detector import EmotionDetector

detector = EmotionDetector()

test_messages = [
    "Feeling Excited about joining the new AI research team, though a bit anxious about the deadlines ahead",
    "I can't believe I failed that test again. I'm so disappointed and frustrated right now",
    "Finally got the job offer! I'm thrilled and can't wait to start this new journey!"
]

for msg in test_messages:
    result = detector.detect_emotions(msg)
    print(f"\nMessage: {msg}")
    print(f"Joy: {result.joy:.2%}")
    print(f"Sadness: {result.sadness:.2%}")
    print(f"Anger: {result.anger:.2%}")
    print(f"Fear: {result.fear:.2%}")
    print(f"Surprise: {result.surprise:.2%}")
    print(f"Anxiety: {result.anxiety:.2%}")
    print(f"Excitement: {result.excitement:.2%}")
    
    # Show top 3 emotions
    emotions = {
        'Joy': result.joy,
        'Sadness': result.sadness,
        'Anger': result.anger,
        'Fear': result.fear,
        'Surprise': result.surprise,
        'Anxiety': result.anxiety,
        'Excitement': result.excitement
    }
    sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
    print(f"Top emotions: {sorted_emotions[0][0]} ({sorted_emotions[0][1]:.2%}), {sorted_emotions[1][0]} ({sorted_emotions[1][1]:.2%}), {sorted_emotions[2][0]} ({sorted_emotions[2][1]:.2%})")

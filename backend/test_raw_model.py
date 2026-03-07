from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir="./models")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir="./models")

test_message = "I can't believe I failed that test again. I'm so disappointed and frustrated right now"

inputs = tokenizer(test_message, return_tensors="pt", truncation=True, max_length=512, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
    scores = scores.cpu().numpy()[0]

labels = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']

print(f"Message: {test_message}\n")
for label, score in zip(labels, scores):
    print(f"{label}: {score:.2%}")

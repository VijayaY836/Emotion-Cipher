from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir="./models")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir="./models")

print("Model config id2label:")
print(model.config.id2label)

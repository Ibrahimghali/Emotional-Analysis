# app/nlp/sentiment_analyzer.py
from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    label = result['label']
    
    if label == "POSITIVE":
        return "positive", result['score']
    elif label == "NEGATIVE":
        return "negative", result['score']
    else:
        return "neutral", result['score']
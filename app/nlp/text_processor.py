# app/nlp/text_processor.py
import re
import emoji
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

# Initialize NLTK resources
def load_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

# Load resources when module is imported
load_nltk_resources()

def clean_text(text):
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove user mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtag symbols (keep the text)
    text = re.sub(r'#', '', text)
    
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    
    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    
    # Remove extra whitespace and normalize line breaks
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def normalize_text(text, remove_stopwords=False):
    if not text:
        return ""
    
    # Clean the text first
    text = clean_text(text)
    
    # Simple tokenization using split instead of word_tokenize
    tokens = text.split()
    
    # Remove stopwords if requested
    if remove_stopwords:
        # Ensure stopwords are loaded
        load_nltk_resources()
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Join tokens back to text
    text = ' '.join(tokens)
    
    return text
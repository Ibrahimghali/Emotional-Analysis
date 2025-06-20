# app/nlp/text_processor.py
import re
import emoji
import unicodedata
import nltk
from nltk.corpus import stopwords
import functools

# Lazy loading of NLTK resources only when needed
@functools.lru_cache(maxsize=1)
def get_stopwords():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    return set(stopwords.words('english'))

def clean_text(text):
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Combine multiple regex operations for better performance
    # Remove URLs, user mentions, hashtag symbols in one pass
    text = re.sub(r'https?://\S+|www\.\S+|@\w+|#', '', text)
    
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    
    # Remove special characters and numbers in one pass
    text = re.sub(r'[^\w\s]|\d+', '', text)
    
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
    
    # Tokenize using simple split - consistent with our needs
    tokens = text.split()
    
    # Remove stopwords if requested (lazy loading)
    if remove_stopwords:
        stop_words = get_stopwords()
        tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back to text
    return ' '.join(tokens)
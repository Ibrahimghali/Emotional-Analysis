# app/nlp/text_processor.py
import re
import emoji
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    # Remove hashtags but keep the text
    text = re.sub(r'#(\w+)', r'\1', text)
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return ' '.join(tokens)
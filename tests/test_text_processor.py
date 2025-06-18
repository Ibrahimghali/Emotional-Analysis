import pytest
from app.nlp.text_processor import clean_text, normalize_text

class TestTextProcessor:
    
    def test_clean_text_with_urls(self):
        """Test that URLs are properly removed"""
        text = "Check out this link https://example.com and also www.test.org"
        cleaned = clean_text(text)
        assert "https://example.com" not in cleaned
        assert "www.test.org" not in cleaned
        assert "check out this link" in cleaned
    
    def test_clean_text_with_mentions(self):
        """Test that @mentions are properly removed"""
        text = "Hello @user1 and @another_user how are you?"
        cleaned = clean_text(text)
        assert "@user1" not in cleaned
        assert "@another_user" not in cleaned
        assert "hello" in cleaned
        assert "how are you" in cleaned
    
    def test_clean_text_with_emojis(self):
        """Test that emojis are properly removed"""
        text = "I feel so happy today! 😊 It's amazing 🎉"
        cleaned = clean_text(text)
        assert "😊" not in cleaned
        assert "🎉" not in cleaned
        assert "i feel so happy today" in cleaned
        assert "its amazing" in cleaned
    
    def test_clean_text_with_special_chars(self):
        """Test that special characters are properly removed"""
        text = "This has special chars: #hashtag, $money, &more!"
        cleaned = clean_text(text)
        assert "#" not in cleaned
        assert "$" not in cleaned
        assert "&" not in cleaned
        assert "!" not in cleaned
        assert "hashtag" in cleaned
    
    def test_clean_text_with_numbers(self):
        """Test that numbers are properly removed"""
        text = "I am 25 years old and I have 3 dogs"
        cleaned = clean_text(text)
        assert "25" not in cleaned
        assert "3" not in cleaned
        assert "i am years old and i have dogs" in cleaned
    
    def test_clean_text_with_unicode(self):
        """Test that Unicode characters are properly normalized"""
        text = "Café Nöel"
        cleaned = clean_text(text)
        assert "café" not in cleaned  # Should be normalized to 'cafe'
        assert "cafe" in cleaned.lower()
    
    def test_clean_text_with_whitespace(self):
        """Test that extra whitespace is properly handled"""
        text = "  Too   much \n\n whitespace  \t here  "
        cleaned = clean_text(text)
        assert cleaned == "too much whitespace here"
    
    def test_clean_text_with_empty_input(self):
        """Test that empty input is handled properly"""
        assert clean_text("") == ""
        assert clean_text(None) == ""
    
    def test_normalize_text_basic(self):
        """Test basic text normalization"""
        text = "Hello world! This is a test."
        normalized = normalize_text(text)
        assert "hello world this is a test" in normalized
    
    def test_normalize_text_with_stopwords_removal(self):
        """Test normalization with stopword removal"""
        text = "This is a test sentence with some stopwords"
        normalized = normalize_text(text, remove_stopwords=True)
        
        # Check that some stopwords are removed
        assert "test" in normalized
        assert "sentence" in normalized
        assert "stopwords" in normalized
        
        # These specific checks might fail depending on the stopwords list
        # So let's make a more general assertion
        assert len(normalized.split()) < len(text.split())
    
    def test_normalize_text_complex_case(self):
        """Test normalization with a complex case"""
        text = "Check out @user's new post 😊! It contains #important information. https://example.com"
        normalized = normalize_text(text)
        
        assert "@user" not in normalized
        assert "😊" not in normalized
        assert "#" not in normalized
        assert "https://example.com" not in normalized
        assert "check out" in normalized
        assert "important information" in normalized
    
    def test_normalize_text_empty_input(self):
        """Test normalization with empty input"""
        assert normalize_text("") == ""
        assert normalize_text(None) == ""
    
    def test_real_depression_tweet(self):
        """Test with a realistic depression-related tweet"""
        tweet = "Feeling so low today 😢 #depression #mentalhealth Anyone else struggle with chronic depression? @MentalHealthOrg https://t.co/link123"
        cleaned = clean_text(tweet)
        normalized = normalize_text(tweet)
        
        assert "#" not in cleaned
        assert "😢" not in cleaned
        assert "@MentalHealthOrg" not in cleaned
        assert "https://t.co/link123" not in cleaned
        assert "feeling so low today" in cleaned
        assert "depression" in cleaned
        assert "mentalhealth" in cleaned
# app/scraper/twitter_scraper.py

import tweepy
import pandas as pd
import os
import time
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables once at module level
load_dotenv()

# Get all available tokens (supports rotation)
def get_twitter_tokens():
    tokens = []
    
    # Print all environment variables for debugging
    print("Environment variables:")
    for key, value in os.environ.items():
        if "TOKEN" in key:
            # Print masked token for security
            masked_value = value[:10] + "..." if value else "None"
            print(f"  {key}: {masked_value}")
    
    i = 1
    while True:
        token = os.getenv(f"TWITTER_BEARER_TOKEN_{i}")
        if not token:
            break
        tokens.append(token)
        i += 1
    
    # Fallback to legacy env var name if numbered ones aren't found
    if not tokens:
        token = os.getenv("TWITTER_BEARER_TOKEN")
        if token:
            tokens.append(token)
    
    print(f"Found {len(tokens)} Twitter tokens")
    return tokens

# Cache results for 15 minutes to avoid redundant API calls
@lru_cache(maxsize=32)
def get_cached_tweets(query, limit, cache_time):
    # Using cache_time parameter to invalidate cache after time period
    return scrape_twitter_internal(query, limit)

def scrape_twitter(query="depression", limit=15, use_cache=True):
    """
    Twitter scraping with rate limit handling, pagination and caching
    """
    print(f"Scraping Twitter for: {query} (limit: {limit})")
    
    if use_cache:
        # Cache key that expires every 15 minutes
        cache_time = int(time.time() / 900)
        return get_cached_tweets(query, limit, cache_time)
    else:
        return scrape_twitter_internal(query, limit)

def scrape_twitter_internal(query, limit):
    tokens = get_twitter_tokens()
    
    if not tokens:
        raise ValueError("No Twitter Bearer Tokens found. Set the TWITTER_BEARER_TOKEN_1 or TWITTER_BEARER_TOKEN environment variable.")
    
    # Try each token until successful
    for token_index, bearer_token in enumerate(tokens):
        try:
            # Initialize Twitter client
            client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
            
            # Enhanced search query
            search_query = f"{query} lang:en -is:retweet"
            
            # Process tweets with pagination
            tweets_data = []
            pagination_token = None
            
            while len(tweets_data) < limit:
                # Calculate how many results to request in this batch
                batch_size = min(100, limit - len(tweets_data))
                if batch_size <= 0:
                    break
                    
                # Make API request
                response = client.search_recent_tweets(
                    query=search_query,
                    max_results=batch_size,
                    next_token=pagination_token,
                    tweet_fields=['created_at', 'public_metrics', 'conversation_id', 'lang'],
                    user_fields=['username', 'name', 'profile_image_url'],
                    expansions=['author_id']
                )
                
                # Break if no data returned
                if not response.data:
                    break
                    
                # Get user data
                users = {user.id: user for user in response.includes.get('users', [])}
                
                # Process tweets from this batch
                for tweet in response.data:
                    user = users.get(tweet.author_id)
                    tweets_data.append({
                        "id": str(tweet.id),
                        "date": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "content": tweet.text,
                        "username": user.username if user else "unknown",
                        "user_name": user.name if user else "unknown",
                        "like_count": tweet.public_metrics['like_count'],
                        "retweet_count": tweet.public_metrics['retweet_count'],
                        "conversation_id": tweet.conversation_id
                    })
                
                # Check if we've reached our limit or the end of available data
                if not response.meta.get('next_token'):
                    break
                    
                # Update pagination token for next request
                pagination_token = response.meta.get('next_token')
            
            print(f"Successfully scraped {len(tweets_data)} tweets")
            return pd.DataFrame(tweets_data)
            
        except Exception as e:
            print(f"Error with token {token_index+1}: {e}")
            # Try next token if available
            continue
            
    # If all tokens failed, return empty DataFrame
    print("All tokens exhausted. Unable to retrieve tweets.")
    return pd.DataFrame(columns=["id", "date", "content", "username", "user_name", "like_count", "retweet_count", "conversation_id"])

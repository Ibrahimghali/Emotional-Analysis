# app/scraper/twitter_scraper.py

import tweepy
import pandas as pd
import os
import time
from dotenv import load_dotenv

def scrape_twitter(query="depression", limit=100):
    """
    Twitter scraping with rate limit handling
    """
    # Load environment variables from .env file
    load_dotenv()
    
    print(f"Scraping Twitter for: {query} (limit: {limit})")
    
    # Get bearer token from environment variable
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    if not bearer_token:
        raise ValueError("Twitter Bearer Token not found. Set the TWITTER_BEARER_TOKEN environment variable.")
    
    # Initialize Twitter client with wait_on_rate_limit=True
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
    
    # Simple search query
    search_query = f"{query} lang:en -is:retweet"
    
    try:
        # Make a single API request with rate limit handling
        response = client.search_recent_tweets(
            query=search_query,
            max_results=min(100, limit),
            tweet_fields=['created_at', 'public_metrics'],
            user_fields=['username'],
            expansions=['author_id']
        )
        
        # Handle case where no tweets are found
        if not response.data:
            print("No tweets found matching the query")
            return pd.DataFrame(columns=["id", "date", "content", "username", "like_count", "retweet_count"])
        
        # Get user data
        users = {user.id: user.username for user in response.includes['users']}
        
        # Process tweets
        tweets_data = []
        for tweet in response.data:
            tweets_data.append({
                "id": str(tweet.id),
                "date": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "content": tweet.text,
                "username": users.get(tweet.author_id, "unknown"),
                "like_count": tweet.public_metrics['like_count'],
                "retweet_count": tweet.public_metrics['retweet_count']
            })
            
            if len(tweets_data) >= limit:
                break
                
        print(f"Successfully scraped {len(tweets_data)} tweets")
        return pd.DataFrame(tweets_data)
        
    except tweepy.TooManyRequests:
        print("Rate limit exceeded. Using previously saved tweets.")
        # Return empty DataFrame - the API will show existing tweets from database
        return pd.DataFrame(columns=["id", "date", "content", "username", "like_count", "retweet_count"])
        
    except Exception as e:
        print(f"Error scraping Twitter: {e}")
        # Return empty DataFrame rather than crashing
        return pd.DataFrame(columns=["id", "date", "content", "username", "like_count", "retweet_count"])

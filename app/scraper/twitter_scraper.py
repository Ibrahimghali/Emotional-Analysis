# app/scraper/twitter_scraper.py

import tweepy
import pandas as pd
import os
from dotenv import load_dotenv

def scrape_twitter(query="depression", limit=100):
    """
    Basic Twitter scraping using bearer token authentication
    """
    # Load environment variables from .env file
    load_dotenv()
    
    print(f"Scraping Twitter for: {query} (limit: {limit})")
    
    # Get bearer token from environment variable
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    if not bearer_token:
        raise ValueError("Twitter Bearer Token not found. Set the TWITTER_BEARER_TOKEN environment variable.")
    
    # Initialize Twitter client
    client = tweepy.Client(bearer_token=bearer_token)
    
    # Simple search query
    search_query = f"{query} lang:en -is:retweet"
    
    try:
        # Make a single API request
        response = client.search_recent_tweets(
            query=search_query,
            max_results=min(100, limit),  # API limit is 100 per request
            tweet_fields=['created_at', 'public_metrics'],
            user_fields=['username'],
            expansions=['author_id']
        )
        
        # Get user data
        users = {user.id: user.username for user in response.includes['users']}
        
        # Process tweets
        tweets_data = []
        for tweet in response.data or []:  # Handle case where no tweets are found
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
        
    except Exception as e:
        print(f"Error scraping Twitter: {e}")
        raise

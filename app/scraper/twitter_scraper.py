# app/scraper/twitter_scraper.py
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
import random

def scrape_twitter(query="depression", limit=100):
    """Generate mock Twitter data for testing"""
    print(f"Generating mock Twitter data for: {query} (limit: {limit})")
    
    # Create sample depression-related tweets
    depression_tweets = [
        "I've been feeling so depressed lately, nothing seems to help #Depression",
        "Anxiety and depression are taking over my life #MentalHealth #Depression",
        "Started therapy this week, hoping it helps with my depression #Recovery",
        "Some days I can't even get out of bed #Depression #MentalHealthAwareness",
        "The support from this community has been amazing for my recovery #Depression",
        "Does anyone else feel completely empty inside? #Depression",
        "My antidepressants finally seem to be working #Depression #Recovery",
        "It's hard to explain depression to someone who's never experienced it",
        "Having a particularly bad day with my depression today #MentalHealth",
        "Finding joy in small things helps with my depression #SelfCare",
    ]
    
    # Generate mock data
    data = []
    now = datetime.now()
    
    for i in range(min(limit, 20)):  # Generate up to 20 mock tweets
        tweet_time = now - timedelta(hours=random.randint(1, 72))
        data.append({
            "id": f"tweet_{i}_{random.randint(10000, 99999)}",
            "date": tweet_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": random.choice(depression_tweets),  # Changed from "text" to "content"
            "username": f"user_{random.randint(100, 999)}",
            "like_count": random.randint(0, 200),
            "retweet_count": random.randint(0, 50)
        })
    
    return pd.DataFrame(data)
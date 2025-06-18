# app/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

# Database connection variables
client = None
db = None

async def init_db():
    """Initialize the database connection"""
    global client, db
    
    # Get MongoDB URL from environment variable or use default Docker Compose service name
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
    
    # Add authentication credentials
    username = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
    password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "password")
    
    # Build the connection string with credentials
    if "://" in mongodb_url and "@" not in mongodb_url:
        # Add credentials if not already in the URL
        parts = mongodb_url.split("://")
        mongodb_url = f"{parts[0]}://{username}:{password}@{parts[1]}"
    
    print(f"Connecting to MongoDB at: {mongodb_url.replace(password, '****')}")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(mongodb_url)
    
    # Use the depression_analysis database
    db_name = os.getenv("MONGO_INITDB_DATABASE", "depression_analysis")
    db = client[db_name]
    
    print(f"Connected to MongoDB database: {db_name}")
    return db

async def get_posts(limit=100):
    """Get posts from the database with a limit"""
    global db
    
    # Fix: Compare with None instead of using boolean evaluation
    if db is None:
        await init_db()
    
    cursor = db.posts.find().limit(limit)
    posts = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string for JSON serialization
    for post in posts:
        post["_id"] = str(post["_id"])
    
    return posts

async def close_db():
    """Close the database connection"""
    global client
    if client is not None:
        client.close()
        print("Closed MongoDB connection")
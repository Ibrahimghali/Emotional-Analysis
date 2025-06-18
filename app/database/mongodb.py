# app/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Database connection variables
client = None
db = None

async def init_db():
    """Initialize the database connection"""
    global client, db
    
    # Connect to MongoDB with credentials from docker-compose
    mongodb_url = "mongodb://admin:password@localhost:27017"
    client = AsyncIOMotorClient(mongodb_url)
    
    # Use the depression_analysis database
    db = client.depression_analysis
    
    print("Connected to MongoDB")
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
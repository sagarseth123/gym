from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os # For potentially using environment variables later

# Default to localhost if not set, but encourage .env or actual strings for dev
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "your_database_name") # IMPORTANT: User must change this or set env var

client: MongoClient | None = None

def connect_and_ping_db():
    global client
    global DB_NAME # Ensure DB_NAME is accessible
    print(f"Attempting to connect to MongoDB: {MONGO_DETAILS} / DB: {DB_NAME}") # Added for clarity
    try:
        client = MongoClient(MONGO_DETAILS, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        client = None

def get_database():
    if client and DB_NAME != "your_database_name": # Basic check
        return client[DB_NAME]
    elif DB_NAME == "your_database_name":
        print("MongoDB error: DB_NAME is still set to the placeholder 'your_database_name'. Please configure it.")
        return None
    else:
        print("MongoDB error: Client not connected or DB_NAME not set properly.")
        return None

# Attempt initial connection when module is loaded,
# but the startup event in main.py will provide clearer logging.
# connect_and_ping_db()
# We will call this explicitly from main.py's startup event instead,
# to ensure logs are captured by Uvicorn correctly.

# Example of how you might get a collection (can be uncommented and used later)
# def get_user_collection():
#     db = get_database()
#     if db:
#         return db.users
#     return None

from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Replace the placeholder with your Atlas connection string
MONGO_DETAILS = "mongodb://localhost:27017" # Placeholder, will be configured later via environment variables

# It's good practice to handle potential connection errors.
try:
    client = MongoClient(MONGO_DETAILS, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None # Set client to None if connection fails

# Placeholder for getting the database
def get_database():
    if client:
        return client.your_database_name # Replace with your actual database name
    return None

# Example of how you might get a collection
# def get_user_collection():
#     db = get_database()
#     if db:
#         return db.users
#     return None

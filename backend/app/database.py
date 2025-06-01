from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database as PyMongoDatabase # Alias to avoid confusion with local 'Database' type hints
from pymongo.server_api import ServerApi
from bson import ObjectId
from typing import Optional, List, Any
import os
from datetime import datetime

# Model Imports
from app.models.user import UserCreate, UserInDB, UserRole
from app.models.gym import GymCreate, GymInDB, GymUpdate # Assuming GymUpdate for gym updates
from app.models.subscription import SubscriptionInDB, SubscriptionCreate # For create_subscription
from app.models.physical_data import PhysicalDataBase # For user's physical data history

# --- Database Connection and Configuration ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "gym_management_db")

client: Optional[MongoClient] = None
db_instance: Optional[PyMongoDatabase] = None

# --- Collection Names ---
USER_COLLECTION = "users"
GYM_COLLECTION = "gyms"
SUBSCRIPTION_COLLECTION = "subscriptions"

def connect_to_mongo():
    global client, db_instance
    print(f"Attempting to connect to MongoDB: {MONGO_URI}")
    try:
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        client.admin.command('ping') # Verify connection
        db_instance = client[DB_NAME]
        print(f"Successfully connected to MongoDB. Database: '{DB_NAME}'")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        client = None
        db_instance = None

def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")

def get_db() -> PyMongoDatabase:
    """
    Returns the PyMongo Database instance.
    Ensures that connect_to_mongo() has been called.
    """
    if db_instance is None:
        print("Warning: get_db() called before MongoDB connection was initialized or connection failed. Attempting to connect now.")
        connect_to_mongo()
        if db_instance is None: # Check again after attempting to connect
            raise Exception("Failed to connect to MongoDB. Database instance is not available.")
    return db_instance

# --- Helper for ObjectId ---
def validate_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise ValueError(f"Invalid ObjectId string: {id_str}")

# --- User CRUD Operations ---
def create_user(db: PyMongoDatabase, user_data: UserCreate, role: UserRole) -> UserInDB:
    user_doc = user_data.model_dump()
    user_doc["role"] = role.value
    user_doc["hashed_password"] = user_data.hashed_password # Already hashed by auth_utils
    user_doc["created_at"] = datetime.utcnow()
    user_doc["updated_at"] = datetime.utcnow()
    # Add default empty physical_data_history if not present in model, UserBase has it
    user_doc.setdefault("physical_data_history", [])
    user_doc.setdefault("address", None)

    result = db[USER_COLLECTION].insert_one(user_doc)
    created_doc = db[USER_COLLECTION].find_one({"_id": result.inserted_id})
    if created_doc:
        return UserInDB(**created_doc)
    raise Exception("Failed to create user or retrieve after creation.")


def get_user_by_email(db: PyMongoDatabase, email: str) -> Optional[UserInDB]:
    user_doc = db[USER_COLLECTION].find_one({"email": email})
    if user_doc:
        return UserInDB(**user_doc)
    return None

def get_user_by_id(db: PyMongoDatabase, user_id: str) -> Optional[UserInDB]:
    try:
        oid = validate_object_id(user_id)
        user_doc = db[USER_COLLECTION].find_one({"_id": oid})
        if user_doc:
            return UserInDB(**user_doc)
    except ValueError: # Invalid ObjectId string
        return None
    return None

# --- Gym CRUD Operations ---
def create_gym(db: PyMongoDatabase, gym_data: GymCreate) -> GymInDB:
    gym_doc = gym_data.model_dump()
    gym_doc["created_at"] = datetime.utcnow()
    gym_doc["updated_at"] = datetime.utcnow()
    # owner_id should be set by the router from current_user.id
    if not gym_doc.get("owner_id"):
        raise ValueError("owner_id is required to create a gym")

    result = db[GYM_COLLECTION].insert_one(gym_doc)
    created_doc = db[GYM_COLLECTION].find_one({"_id": result.inserted_id})
    if created_doc:
        return GymInDB(**created_doc)
    raise Exception("Failed to create gym or retrieve after creation.")


def get_gym_by_id(db: PyMongoDatabase, gym_id: str) -> Optional[GymInDB]:
    try:
        oid = validate_object_id(gym_id)
        gym_doc = db[GYM_COLLECTION].find_one({"_id": oid})
        if gym_doc:
            return GymInDB(**gym_doc)
    except ValueError:
        return None
    return None

def update_gym_details(db: PyMongoDatabase, gym_id: str, gym_update_data: GymUpdate) -> Optional[GymInDB]:
    try:
        oid = validate_object_id(gym_id)
        update_doc = gym_update_data.model_dump(exclude_unset=True) # Use exclude_unset for partial updates
        update_doc["updated_at"] = datetime.utcnow()

        updated_doc = db[GYM_COLLECTION].find_one_and_update(
            {"_id": oid},
            {"$set": update_doc},
            return_document=ReturnDocument.AFTER
        )
        if updated_doc:
            return GymInDB(**updated_doc)
    except ValueError:
        return None
    return None

def delete_gym_by_id(db: PyMongoDatabase, gym_id: str) -> bool:
    try:
        oid = validate_object_id(gym_id)
        result = db[GYM_COLLECTION].delete_one({"_id": oid})
        return result.deleted_count > 0
    except ValueError:
        return False

# --- Subscription CRUD Operations ---
def create_subscription(db: PyMongoDatabase, subscription_data: SubscriptionCreate) -> SubscriptionInDB:
    sub_doc = subscription_data.model_dump()
    sub_doc["created_at"] = datetime.utcnow() # Assuming model might have this
    sub_doc["updated_at"] = datetime.utcnow()

    # Ensure user_id and gym_id are valid ObjectIds if they are stored as such
    # For this implementation, assuming they are strings that might represent ObjectIds or other keys
    # If they need to be ObjectIds in DB, conversion logic would be needed here.
    # For now, models define them as str, so direct storage is fine.

    result = db[SUBSCRIPTION_COLLECTION].insert_one(sub_doc)
    created_doc = db[SUBSCRIPTION_COLLECTION].find_one({"_id": result.inserted_id})
    if created_doc:
        return SubscriptionInDB(**created_doc)
    raise Exception("Failed to create subscription or retrieve after creation.")

def get_subscriptions_by_gym_id(db: PyMongoDatabase, gym_id: str) -> List[SubscriptionInDB]:
    # Assuming gym_id in Subscription model is a string that could be an ObjectId string or other gym identifier
    # If gym_id in subscriptions collection is stored as ObjectId, this query needs adjustment.
    # For now, assume it's stored as the string version of the Gym's ObjectId or another string key.
    # The GymInDB model has id as string, so gym.id will be string.
    subscriptions_cursor = db[SUBSCRIPTION_COLLECTION].find({"gym_id": gym_id})
    return [SubscriptionInDB(**sub_doc) for sub_doc in subscriptions_cursor]

# Note on ObjectId handling in Pydantic models:
# UserInDB, GymInDB, SubscriptionInDB all have:
#   id: str = Field(..., alias="_id")
# And in their Config:
#   allow_population_by_field_name = True
#   json_encoders = { ObjectId: str } or handle ObjectId conversion before passing to model.
# Pydantic should handle _id: ObjectId from DB to id: str in model if ObjectId is serializable.
# The default Pydantic behavior with allow_population_by_field_name=True and alias="_id" for an `id: str` field
# typically handles the ObjectId from MongoDB correctly by calling str(ObjectId).
# If `arbitrary_types_allowed = True` is also in model Config, it's even more flexible.
# The models used (e.g. UserInDB) already have this structure from previous steps.
# Make sure `physical_data_history` in User model is handled correctly if it involves conversion.
# User model has List[PhysicalData], PhysicalData is PhysicalDataBase. These are embedded, so direct pymongo types should map.
# (e.g. datetime from pymongo to datetime in pydantic).
# The `hashed_password` in `UserCreate` is used directly in `create_user` as it's pre-hashed.
# The `GymUpdate` model is used in `update_gym_details` as requested.
# The `SubscriptionCreate` model is used in `create_subscription`.

# Ensure all router dependencies for DB are updated to pass `PyMongoDatabase` instance.
# The `get_db()` function now returns `PyMongoDatabase`.
# The `Depends(get_db_session)` in routers needs to provide this.
# The `get_db_session` in routers was a placeholder; it calls `get_db()`. This should align.
# If `get_db_session` is async, but `get_db` is sync, it's okay for now.
# A true async setup would use an async MongoDB driver (e.g., Motor) and async def for DB functions.
# This subtask focuses on replacing placeholders with PyMongo (sync) logic.
# The `Any` type hint for `db` in old placeholder functions will now be `PyMongoDatabase`.
# Routers using `db: Any = Depends(get_db_session)` will have `get_db_session` provide `PyMongoDatabase`.

# The prepopulation functions (_prepopulate_users, _prepopulate_subscriptions_and_gyms)
# and the fake stores (_FAKE_USER_DB_STORE, etc.) are now removed.
# Testing will require manual data insertion or API calls.
# Renamed placeholder functions in routers need to be updated (e.g. get_user_by_id_placeholder -> get_user_by_id)
# This will be done in the next step.
# For this step, the database.py file itself is the focus.
print("Database module (database.py) reloaded with MongoDB implementations.")

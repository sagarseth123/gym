from fastapi.testclient import TestClient
from pymongo.database import Database as PyMongoDatabase
from typing import Dict, Optional

from backend.app.models.user import UserCreate, UserRole
from backend.app.models.gym import GymCreate
from backend.app.database import create_user as db_create_user # Renamed to avoid clash
from backend.app.database import create_gym as db_create_gym # Renamed
from backend.app.auth_utils import hash_password # To hash password for direct DB insertion

# --- Auth Helpers ---
def get_admin_auth_headers(
    client: TestClient,
    admin_email: str = "testadmin@example.com",
    admin_password: str = "testadminpassword"
) -> Dict[str, str]:
    """
    Logs in an admin user and returns authorization headers.
    Assumes the admin user already exists or is created by a fixture/setup.
    """
    login_data = {
        "username": admin_email,
        "password": admin_password,
    }
    response = client.post("/auth/login/admin", data=login_data)
    if response.status_code != 200:
        # Optionally, print response.json() for debugging
        # print(f"Login failed: {response.json()}")
        raise Exception(f"Admin login failed with status {response.status_code}")

    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

# --- User Creation Helper ---
def create_test_admin_user(
    db: PyMongoDatabase,
    email: str = "testadmin@example.com",
    password: str = "testadminpassword",
    full_name: Optional[str] = "Test Admin User"
) -> Dict: # Returns the user document from DB
    """
    Creates an admin user directly in the database for testing.
    Returns the created user document (dict).
    """
    # Check if user already exists to avoid duplicate key errors if email is unique index
    existing_user = db["users"].find_one({"email": email})
    if existing_user:
        # For testing, it might be okay to return the existing user or raise an error
        # print(f"User {email} already exists. Returning existing.")
        # To ensure UserInDB compatibility, make sure all fields are present
        # This might not be a UserInDB instance but a dict from DB.
        return existing_user

    hashed_pw = hash_password(password)
    user_create = UserCreate(
        email=email,
        full_name=full_name,
        hashed_password=hashed_pw, # This field is named 'hashed_password' in UserCreate
        role=UserRole.admin, # This field is part of UserBase, UserCreate inherits it
        is_active=True,
        address="123 Test St" # Example address
    )
    # The db_create_user function in database.py expects UserCreate and role separately
    created_user_model = db_create_user(db=db, user_data=user_create, role=UserRole.admin)

    # Fetch the raw document from DB to ensure it's what's actually stored, including _id
    user_doc = db["users"].find_one({"email": email})
    if not user_doc:
        raise Exception("Failed to create or find test admin user in DB after creation call.")
    return user_doc


# --- Gym Creation Helper ---
def create_test_gym(
    db: PyMongoDatabase,
    owner_id: str, # This should be the string representation of User's ObjectId
    gym_name: str = "Test Gym"
) -> Dict: # Returns the gym document from DB
    """
    Creates a gym directly in the database for testing.
    owner_id should be the string version of the User's MongoDB _id.
    Returns the created gym document (dict).
    """
    gym_create = GymCreate(
        name=gym_name,
        owner_id=owner_id, # GymCreate model expects owner_id
        address="100 Test Road",
        city="Testville"
        # Add other fields from GymCreate as needed for tests
    )
    # The db_create_gym function in database.py expects GymCreate
    created_gym_model = db_create_gym(db=db, gym_data=gym_create)

    gym_doc = db["gyms"].find_one({"name": gym_name, "owner_id": owner_id})
    if not gym_doc:
        raise Exception("Failed to create or find test gym in DB after creation call.")
    return gym_doc

# Note: Helper functions returning MongoDB documents (dicts) are often more useful for tests
# as they reflect the actual stored data. Pydantic models can be instantiated from these dicts
# in tests if needed (e.g., `UserInDB(**user_doc)`).
# The user_id and gym_id in models are typically string representations of ObjectId.
# Ensure owner_id passed to create_test_gym is a string (user_doc['_id'] is ObjectId, so str(user_doc['_id'])).

import pytest
from fastapi.testclient import TestClient
from pymongo.database import Database as PyMongoDatabase

# Adjust the import path according to your project structure
# This assumes 'app' is a top-level directory alongside 'tests'
# or that the backend directory is in PYTHONPATH.
from backend.app.main import app # Import your FastAPI app instance
from backend.app.database import connect_to_mongo, close_mongo_connection, get_db, DB_NAME, USER_COLLECTION, GYM_COLLECTION, SUBSCRIPTION_COLLECTION

@pytest.fixture(scope="session") # session scope for DB connection
def db_connection():
    """
    Manages MongoDB connection for the test session.
    Connects before tests start, disconnects after they finish.
    """
    print(f"Connecting to MongoDB for test session (DB: {DB_NAME})...")
    connect_to_mongo() # Establish connection
    yield
    print("\nClosing MongoDB connection after test session...")
    close_mongo_connection() # Close connection

@pytest.fixture(scope="function") # function scope for db session to ensure it's fresh if needed
def db_session(db_connection): # Depends on the session-scoped connection manager
    """
    Provides a PyMongo Database session for a test function.
    Optionally, can implement per-test data cleanup here if needed in future.
    For now, it just returns the db_instance.
    """
    db = get_db()
    # Example: Clean up specific collections before each test (if desired)
    # print(f"Clearing test collections in {DB_NAME} for test function...")
    # db[USER_COLLECTION].delete_many({})
    # db[GYM_COLLECTION].delete_many({})
    # db[SUBSCRIPTION_COLLECTION].delete_many({})
    # This cleanup is commented out as per subtask instructions (manage own data)
    return db

@pytest.fixture(scope="function")
def client(db_session): # Ensure db_session (and thus db_connection) is set up before client
    """
    Provides a TestClient instance for making API requests in tests.
    It uses the FastAPI app instance.
    """
    # The TestClient can be used to make requests to your application.
    # Startup/shutdown events of the app (like DB connection) should be handled.
    # FastAPI's TestClient typically handles startup/shutdown events.
    with TestClient(app) as c:
        yield c

# Note: The db_connection fixture establishes the DB connection once per session.
# The db_session fixture provides the 'db' object (PyMongoDatabase instance) to each test function.
# If tests need to be strictly isolated data-wise, clearing collections in db_session
# (or using different databases/collections per test) would be necessary.
# The current setup relies on tests using unique data to avoid conflicts.
# The `connect_to_mongo` in `database.py` should ideally be idempotent or safe to call multiple times
# if TestClient also triggers app startup events that might call it.
# Our current `connect_to_mongo` sets global `client` and `db_instance`, so it's mostly fine.

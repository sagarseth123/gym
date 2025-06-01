from fastapi.testclient import TestClient
from pymongo.database import Database as PyMongoDatabase
import pytest # For marking tests, using fixtures

from backend.app.models.user import UserCreate, UserRole # For type hinting if needed
from backend.tests.utils import create_test_admin_user # To create a user for login tests

# --- Test Admin Signup ---
def test_admin_signup_success(client: TestClient, db_session: PyMongoDatabase):
    # Ensure fresh DB state for this test if needed, or use unique email
    # For now, assuming this email is not already in DB from other tests or manual setup
    unique_email = "newadmin@example.com"
    response = client.post(
        "/auth/signup/admin",
        json={
            "email": unique_email,
            "full_name": "New Admin",
            "hashed_password": "newpassword123", # UserCreate expects 'hashed_password' for plain pass
            "role": UserRole.admin.value, # UserCreate expects role
            "is_active": True,
            "address": "789 Admin Ave"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert data["full_name"] == "New Admin"
    assert data["role"] == UserRole.admin.value
    assert data["is_active"] is True
    assert "id" in data

    # Verify user in DB (optional, but good for thoroughness)
    user_in_db = db_session["users"].find_one({"email": unique_email})
    assert user_in_db is not None
    assert user_in_db["role"] == UserRole.admin.value

def test_admin_signup_existing_email(client: TestClient, db_session: PyMongoDatabase):
    # Create a user first (or use one known to exist)
    existing_email = "existingadmin@example.com"
    create_test_admin_user(db_session, email=existing_email, password="password")

    response = client.post(
        "/auth/signup/admin",
        json={
            "email": existing_email, # Attempt to sign up with the same email
            "full_name": "Another Admin",
            "hashed_password": "anotherpassword",
            "role": UserRole.admin.value,
            "is_active": True,
        },
    )
    assert response.status_code == 400 # Bad Request or Conflict
    data = response.json()
    assert "Email already registered" in data["detail"]


# --- Test Admin Login ---
def test_admin_login_success(client: TestClient, db_session: PyMongoDatabase):
    admin_email = "loginadmin@example.com"
    admin_password = "loginpassword123"
    # Ensure this user exists for the login test
    create_test_admin_user(db_session, email=admin_email, password=admin_password)

    response = client.post(
        "/auth/login/admin",
        data={"username": admin_email, "password": admin_password}, # OAuth2PasswordRequestForm format
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_admin_login_incorrect_password(client: TestClient, db_session: PyMongoDatabase):
    admin_email = "loginadmin_wrongpass@example.com"
    admin_password = "correctpassword"
    # Ensure user exists
    create_test_admin_user(db_session, email=admin_email, password=admin_password)

    response = client.post(
        "/auth/login/admin",
        data={"username": admin_email, "password": "incorrectpassword"},
    )
    assert response.status_code == 401 # Unauthorized
    data = response.json()
    assert "Incorrect email or password" in data["detail"]

def test_admin_login_non_existent_user(client: TestClient):
    response = client.post(
        "/auth/login/admin",
        data={"username": "nonexistent@example.com", "password": "anypassword"},
    )
    assert response.status_code == 401 # Unauthorized
    data = response.json()
    # The message might be generic to avoid user enumeration
    assert "Incorrect email or password" in data["detail"]

# --- (Optional) Test Google OAuth Stubs ---
# These tests would just check if the stubs return their placeholder messages correctly.
def test_google_login_stub(client: TestClient):
    response = client.get("/auth/google/login")
    assert response.status_code == 200
    assert "Google login initiated" in response.json()["message"]

def test_google_callback_stub_no_code(client: TestClient):
    response = client.get("/auth/google/callback") # No code provided
    assert response.status_code == 400 # Bad Request due to missing code
    assert "Missing authorization code" in response.json()["detail"]

def test_google_callback_stub_with_code(client: TestClient, db_session: PyMongoDatabase):
    # This test depends on the stub's logic for creating a user if not found.
    # The stub currently creates a user like "user_{code}@example.com".
    # If this user is created, subsequent calls with the same code might behave differently
    # if the stub doesn't handle existing "Google users" uniquely on each call.
    # For a simple stub, we just check if it processes and returns a token.
    test_code = "testauthcode123"
    response = client.get(f"/auth/google/callback?code={test_code}")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == f"user_{test_code}@example.com" # As per stub logic
    # Verify user created in DB by the stub
    user_in_db = db_session["users"].find_one({"email": f"user_{test_code}@example.com"})
    assert user_in_db is not None
    assert user_in_db["google_id"] == f"google_id_{test_code}"

def test_google_callback_stub_with_error(client: TestClient):
    response = client.get("/auth/google/callback?error=access_denied")
    assert response.status_code == 400 # Bad Request due to error param
    assert "Google OAuth error: access_denied" in response.json()["detail"]

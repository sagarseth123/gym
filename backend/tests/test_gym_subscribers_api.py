from fastapi.testclient import TestClient
from pymongo.database import Database as PyMongoDatabase
import pytest
from typing import Dict, List # Added List
import uuid
from datetime import datetime, timedelta

from backend.tests.utils import get_admin_auth_headers, create_test_admin_user, create_test_gym
from backend.app.models.user import UserCreate, UserRole
from backend.app.models.subscription import SubscriptionCreate
from backend.app.database import (
    create_user as db_create_user,
    create_subscription as db_create_subscription,
    USER_COLLECTION, SUBSCRIPTION_COLLECTION, GYM_COLLECTION # For cleanup if needed
)

# --- Test Data Generation ---
def unique_email(prefix="subscriber"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

def unique_gym_name(prefix="SubGym"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"

# --- Fixtures ---
@pytest.fixture(scope="module")
def gym_owner_data(db_session: PyMongoDatabase):
    email = unique_email("gymowner")
    password = "ownerpassword"
    user_doc = create_test_admin_user(db_session, email=email, password=password, full_name="Gym Owner")
    # Convert ObjectId to str for owner_id, as models expect str for IDs from API/Pydantic context
    return {"email": email, "password": password, "user_id": str(user_doc["_id"]), "user_doc": user_doc}

@pytest.fixture(scope="module")
def gym_owner_headers(client: TestClient, gym_owner_data: Dict):
    return get_admin_auth_headers(client, admin_email=gym_owner_data["email"], admin_password=gym_owner_data["password"])

@pytest.fixture(scope="function") # Function scope to create a fresh gym for each test needing it
def test_gym(db_session: PyMongoDatabase, gym_owner_data: Dict) -> Dict:
    gym_doc = create_test_gym(db_session, owner_id=gym_owner_data["user_id"], gym_name=unique_gym_name())
    # Return document with _id as str for API usage
    gym_doc["_id"] = str(gym_doc["_id"])
    return gym_doc

# --- Subscriber Viewing Tests ---

def test_view_subscribers_success(
    client: TestClient, db_session: PyMongoDatabase, test_gym: Dict, gym_owner_headers: Dict
):
    gym_id_str = test_gym["_id"]

    # Create subscriber users
    subscriber1_email = unique_email("sub1")
    subscriber1_doc = db_create_user(db_session, UserCreate(email=subscriber1_email, hashed_password="subpassword", role=UserRole.user), role=UserRole.user)
    subscriber1_id_str = str(subscriber1_doc.id) # UserInDB returns id as str

    subscriber2_email = unique_email("sub2")
    subscriber2_doc = db_create_user(db_session, UserCreate(email=subscriber2_email, hashed_password="subpassword", role=UserRole.user), role=UserRole.user)
    subscriber2_id_str = str(subscriber2_doc.id)

    # Create subscriptions for these users to the test_gym
    db_create_subscription(db_session, SubscriptionCreate(
        user_id=subscriber1_id_str, gym_id=gym_id_str, plan_name="Gold Plan",
        start_date=datetime.utcnow() - timedelta(days=10),
        end_date=datetime.utcnow() + timedelta(days=20), is_active=True
    ))
    db_create_subscription(db_session, SubscriptionCreate(
        user_id=subscriber2_id_str, gym_id=gym_id_str, plan_name="Silver Plan",
        start_date=datetime.utcnow() - timedelta(days=5),
        end_date=datetime.utcnow() + timedelta(days=25), is_active=False # One active, one not
    ))

    response = client.get(f"/admin/gyms/{gym_id_str}/subscribers", headers=gym_owner_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    # Check details (order might vary, so check for presence)
    emails_in_response = {item["email"] for item in data}
    assert subscriber1_email in emails_in_response
    assert subscriber2_email in emails_in_response

    for item in data:
        if item["email"] == subscriber1_email:
            assert item["plan_name"] == "Gold Plan"
            assert item["subscription_is_active"] is True
            assert item["latest_physical_data"] is not None # User model populates some by default
        elif item["email"] == subscriber2_email:
            assert item["plan_name"] == "Silver Plan"
            assert item["subscription_is_active"] is False


def test_view_subscribers_empty_gym(
    client: TestClient, test_gym: Dict, gym_owner_headers: Dict
):
    gym_id_str = test_gym["_id"]
    response = client.get(f"/admin/gyms/{gym_id_str}/subscribers", headers=gym_owner_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_view_subscribers_non_owner_admin_forbidden(
    client: TestClient, db_session: PyMongoDatabase, test_gym: Dict # test_gym owned by gym_owner_data
):
    # Create a different admin
    other_admin_email = unique_email("otheradmin_nosubview")
    other_admin_password = "otherpassword"
    create_test_admin_user(db_session, email=other_admin_email, password=other_admin_password)
    other_admin_headers = get_admin_auth_headers(client, admin_email=other_admin_email, admin_password=other_admin_password)

    gym_id_str = test_gym["_id"]
    response = client.get(f"/admin/gyms/{gym_id_str}/subscribers", headers=other_admin_headers)
    assert response.status_code == 403 # Forbidden


def test_view_subscribers_unauthenticated(client: TestClient, test_gym: Dict):
    gym_id_str = test_gym["_id"]
    response = client.get(f"/admin/gyms/{gym_id_str}/subscribers") # No headers
    assert response.status_code == 401 # Unauthorized


def test_view_subscribers_non_existent_gym(client: TestClient, gym_owner_headers: Dict):
    non_existent_gym_id = "60d5ecf0e7a2e8a0a0000003"
    response = client.get(f"/admin/gyms/{non_existent_gym_id}/subscribers", headers=gym_owner_headers)
    assert response.status_code == 404 # Dependency get_gym_owner_verified should raise 404

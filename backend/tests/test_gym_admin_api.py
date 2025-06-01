from fastapi.testclient import TestClient
from pymongo.database import Database as PyMongoDatabase
import pytest
from typing import Dict
import uuid # For generating unique names/emails in tests

from backend.tests.utils import get_admin_auth_headers, create_test_admin_user, create_test_gym
from backend.app.models.gym import GymUpdate # For update payload

# --- Test Data Generation ---
def unique_email(prefix="testuser"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

def unique_gym_name(prefix="Test Gym"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"

# --- Fixture for a test admin and their headers ---
@pytest.fixture(scope="module") # Module scope: one admin user per test module run
def admin_user_data(db_session: PyMongoDatabase):
    email = unique_email("moduleadmin")
    password = "moduleadminpassword"
    user_doc = create_test_admin_user(db_session, email=email, password=password)
    return {"email": email, "password": password, "user_doc": user_doc}

@pytest.fixture(scope="module")
def admin_headers(client: TestClient, admin_user_data: Dict):
    return get_admin_auth_headers(client, admin_email=admin_user_data["email"], admin_password=admin_user_data["password"])

# --- Gym Management Tests ---

def test_create_gym_success(client: TestClient, db_session: PyMongoDatabase, admin_headers: Dict, admin_user_data: Dict):
    gym_name = unique_gym_name()
    response = client.post(
        "/admin/gyms",
        headers=admin_headers,
        json={"name": gym_name, "address": "123 Test St", "city": "Testville"} # owner_id set by server
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == gym_name
    assert data["owner_id"] == str(admin_user_data["user_doc"]["_id"]) # owner_id is str in response
    assert "id" in data

    gym_in_db = db_session["gyms"].find_one({"_id": data["id"]}) # In DB, _id is ObjectId, but data["id"] is str
    # The database.py get_gym_by_id handles string ID to ObjectId conversion for lookup
    # For direct DB check here, we need to use find_one({"_id": ObjectId(data["id"])}) if data["id"] is string
    # However, GymPublic returns 'id' as string. create_gym in database.py returns GymInDB where id is also string.
    # Let's assume data["id"] is the string version of ObjectId.
    # The create_gym in database.py returns GymInDB which should have id (string) and _id (ObjectId)
    # The response model GymPublic has id: str.
    # For this test, if data["id"] is from GymPublic, it's a string.
    # The create_gym function returns GymInDB which has `id: str = Field(..., alias="_id")`
    # So data["id"] from response should be the string form of the ObjectId.
    gym_in_db_direct = db_session["gyms"].find_one({"name": gym_name}) # Check by unique name for simplicity
    assert gym_in_db_direct is not None
    assert str(gym_in_db_direct["owner_id"]) == str(admin_user_data["user_doc"]["_id"])


def test_create_gym_unauthenticated(client: TestClient):
    response = client.post(
        "/admin/gyms",
        json={"name": "Unauthorized Gym", "address": "Some St", "city": "SomeCity"}
    )
    assert response.status_code == 401 # Unauthorized


def test_get_gym_success(client: TestClient, db_session: PyMongoDatabase, admin_headers: Dict, admin_user_data: Dict):
    owner_id_str = str(admin_user_data["user_doc"]["_id"])
    gym_name = unique_gym_name("OwnedGym")
    gym_doc = create_test_gym(db_session, owner_id=owner_id_str, gym_name=gym_name)
    gym_id_str = str(gym_doc["_id"])

    response = client.get(f"/admin/gyms/{gym_id_str}", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == gym_name
    assert data["id"] == gym_id_str


def test_get_another_admins_gym_allowed(client: TestClient, db_session: PyMongoDatabase, admin_headers: Dict):
    # Create another admin and their gym
    other_admin_email = unique_email("otheradmin")
    other_admin_doc = create_test_admin_user(db_session, email=other_admin_email, password="otherpassword")
    other_admin_id_str = str(other_admin_doc["_id"])

    other_gym_name = unique_gym_name("OtherAdminsGym")
    other_gym_doc = create_test_gym(db_session, owner_id=other_admin_id_str, gym_name=other_gym_name)
    other_gym_id_str = str(other_gym_doc["_id"])

    # Current admin (from admin_headers) tries to get this other gym
    response = client.get(f"/admin/gyms/{other_gym_id_str}", headers=admin_headers)
    assert response.status_code == 200 # Admins can view any gym as per current setup
    data = response.json()
    assert data["name"] == other_gym_name
    assert data["id"] == other_gym_id_str


def test_get_non_existent_gym(client: TestClient, admin_headers: Dict):
    non_existent_gym_id = "60d5ecf0e7a2e8a0a0000000" # Valid ObjectId format, but non-existent
    response = client.get(f"/admin/gyms/{non_existent_gym_id}", headers=admin_headers)
    assert response.status_code == 404


def test_update_own_gym_success(client: TestClient, db_session: PyMongoDatabase, admin_headers: Dict, admin_user_data: Dict):
    owner_id_str = str(admin_user_data["user_doc"]["_id"])
    gym_name = unique_gym_name("UpdatableGym")
    gym_doc = create_test_gym(db_session, owner_id=owner_id_str, gym_name=gym_name)
    gym_id_str = str(gym_doc["_id"])

    update_payload = GymUpdate(name="Updated Gym Name", city="UpdatedCity").model_dump(exclude_unset=True)
    response = client.put(f"/admin/gyms/{gym_id_str}", headers=admin_headers, json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Gym Name"
    assert data["city"] == "UpdatedCity"
    assert data["id"] == gym_id_str

    # Verify in DB
    updated_gym_in_db = db_session["gyms"].find_one({"_id": gym_doc["_id"]})
    assert updated_gym_in_db["name"] == "Updated Gym Name"


def test_update_gym_by_non_owner_admin_forbidden(client: TestClient, db_session: PyMongoDatabase, admin_headers: Dict):
    # Create another admin and their gym
    other_admin_email = unique_email("otheradmin_update")
    other_admin_doc = create_test_admin_user(db_session, email=other_admin_email, password="otherpassword")
    other_admin_id_str = str(other_admin_doc["_id"])

    other_gym_doc = create_test_gym(db_session, owner_id=other_admin_id_str, gym_name=unique_gym_name("OtherGymToUpdate"))
    other_gym_id_str = str(other_gym_doc["_id"])

    # Current admin (from admin_headers) tries to update this other gym
    update_payload = {"name": "Attempted Update"}
    response = client.put(f"/admin/gyms/{other_gym_id_str}", headers=admin_headers, json=update_payload)
    assert response.status_code == 403 # Forbidden


def test_update_gym_unauthenticated(client: TestClient, db_session: PyMongoDatabase, admin_user_data: Dict):
    owner_id_str = str(admin_user_data["user_doc"]["_id"]) # Use main admin's ID for gym creation
    gym_doc = create_test_gym(db_session, owner_id=owner_id_str, gym_name=unique_gym_name("UnauthUpdateGym"))
    gym_id_str = str(gym_doc["_id"])

    update_payload = {"name": "Unauth Update Attempt"}
    response = client.put(f"/admin/gyms/{gym_id_str}", json=update_payload) # No headers
    assert response.status_code == 401 # Unauthorized


def test_update_non_existent_gym(client: TestClient, admin_headers: Dict):
    non_existent_gym_id = "60d5ecf0e7a2e8a0a0000001"
    update_payload = {"name": "Update Non Existent"}
    response = client.put(f"/admin/gyms/{non_existent_gym_id}", headers=admin_headers, json=update_payload)
    assert response.status_code == 404 # Dependency get_gym_owner_verified should raise 404 if gym not found


def test_delete_own_gym_success(client: TestClient, db_session: PyMongoDatabase, admin_headers: Dict, admin_user_data: Dict):
    owner_id_str = str(admin_user_data["user_doc"]["_id"])
    gym_name = unique_gym_name("DeletableGym")
    gym_doc = create_test_gym(db_session, owner_id=owner_id_str, gym_name=gym_name)
    gym_id_str = str(gym_doc["_id"])

    response = client.delete(f"/admin/gyms/{gym_id_str}", headers=admin_headers)
    assert response.status_code == 204 # No Content

    # Verify in DB
    deleted_gym_in_db = db_session["gyms"].find_one({"_id": gym_doc["_id"]})
    assert deleted_gym_in_db is None


def test_delete_gym_by_non_owner_admin_forbidden(client: TestClient, db_session: PyMongoDatabase, admin_headers: Dict):
    other_admin_email = unique_email("otheradmin_delete")
    other_admin_doc = create_test_admin_user(db_session, email=other_admin_email, password="otherpassword")
    other_admin_id_str = str(other_admin_doc["_id"])

    other_gym_doc = create_test_gym(db_session, owner_id=other_admin_id_str, gym_name=unique_gym_name("OtherGymToDelete"))
    other_gym_id_str = str(other_gym_doc["_id"])

    response = client.delete(f"/admin/gyms/{other_gym_id_str}", headers=admin_headers)
    assert response.status_code == 403 # Forbidden


def test_delete_gym_unauthenticated(client: TestClient, db_session: PyMongoDatabase, admin_user_data: Dict):
    owner_id_str = str(admin_user_data["user_doc"]["_id"])
    gym_doc = create_test_gym(db_session, owner_id=owner_id_str, gym_name=unique_gym_name("UnauthDeleteGym"))
    gym_id_str = str(gym_doc["_id"])

    response = client.delete(f"/admin/gyms/{gym_id_str}") # No headers
    assert response.status_code == 401 # Unauthorized


def test_delete_non_existent_gym(client: TestClient, admin_headers: Dict):
    non_existent_gym_id = "60d5ecf0e7a2e8a0a0000002"
    response = client.delete(f"/admin/gyms/{non_existent_gym_id}", headers=admin_headers)
    assert response.status_code == 404 # Dependency should raise 404

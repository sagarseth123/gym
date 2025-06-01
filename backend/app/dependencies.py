from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pymongo.database import Database as PyMongoDatabase # Import PyMongoDatabase
import logging # For logging

from app.auth_utils import decode_access_token
# Updated database imports
from app.database import get_user_by_email, get_gym_by_id, get_db # Import get_db for session
from app.models.user import UserInDB, UserRole
from app.models.gym import GymInDB

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/admin")

# DB Session Dependency for dependencies.py
# This is similar to what's in routers, ensuring dependencies also get a DB session.
async def get_db_session_for_dependencies() -> PyMongoDatabase:
    try:
        db = get_db()
        return db
    except Exception as e:
        logging.error(f"Database connection error in get_db_session_for_dependencies: {e}")
        # Re-raise or handle as appropriate for dependencies
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection failed (dependency).")


async def get_current_user_base(
    token: str = Depends(oauth2_scheme),
    db: PyMongoDatabase = Depends(get_db_session_for_dependencies)
) -> UserInDB:
    """
    Decodes token, gets user, and performs basic validation.
    'db' would be a database session if using a real database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user_base)) -> UserInDB:
    """
    Ensures the user fetched from token is active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

async def get_current_active_admin_user(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    """
    Ensures the active user has the 'admin' role.
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have administrative privileges.",
        )
    return current_user

async def get_gym_owner_verified(
    gym_id: str = Path(..., description="The ID of the gym to retrieve"),
    current_user: UserInDB = Depends(get_current_active_admin_user), # This already calls get_current_active_user -> get_current_user_base which gets db session
    db: PyMongoDatabase = Depends(get_db_session_for_dependencies) # Explicitly get db session here as well
) -> GymInDB:
    """
    Retrieves a gym by its ID and verifies that the current admin user is its owner.
    """
    gym = get_gym_by_id(db=db, gym_id=gym_id)
    if not gym:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found")

    # Check if owner_id is populated. If GymCreate doesn't require it from client,
    # it should be set by the server during creation.
    if not gym.owner_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gym record is missing owner information.")

    if gym.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to modify this gym.",
        )
    return gym

# Note: `get_current_active_admin_user` itself depends on `get_current_active_user`,
# which depends on `get_current_user_base`. `get_current_user_base` now correctly
# gets a `PyMongoDatabase` session via `Depends(get_db_session_for_dependencies)`.
# So `current_user` is already populated using a DB session.
# The `db: PyMongoDatabase = Depends(get_db_session_for_dependencies)` in `get_gym_owner_verified`
# ensures this specific function also has direct access to a DB session if needed for its own operations,
# which it does for `get_gym_by_id`.

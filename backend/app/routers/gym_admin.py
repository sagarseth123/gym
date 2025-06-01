from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from typing import List, Any, Optional

from app.models.gym import GymCreate, GymPublic, GymInDB, GymUpdate
from app.models.user import UserInDB
from app.models.subscription import SubscriptionInDB # For type hint
from app.models.physical_data import PhysicalDataBase # For type hint
from app.schemas.user import SubscribedUserDetail # Import the new response schema
from app.dependencies import get_current_active_admin_user, get_gym_owner_verified
from app.database import (
    create_gym, # Updated import
    get_gym_by_id, # Updated import
    update_gym_details, # Updated import
    delete_gym_by_id, # Updated import
    get_subscriptions_by_gym_id, # Updated import
    get_user_by_id, # Updated import
    get_db
)

router = APIRouter()

# DB Session Dependency for this router
async def get_db_session(): # Renamed from placeholder in thought process to avoid confusion
    try:
        # In a real scenario, this would yield an actual DB session
        # For placeholder functions, this might not be strictly needed if they use a global store
        # or if get_db() itself manages the connection adequately for sync operations.
        db = get_db() # Assuming get_db() from database.py is sufficient for placeholders
        return db
    except Exception as e:
        # Consider logging the exception e
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection error.")

@router.post(
    "/gyms",
    response_model=GymPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Gym",
    description="Allows an authenticated admin user to create a new gym. The `owner_id` will be automatically set to the ID of the logged-in admin."
)
async def create_new_gym(
    gym_data: GymCreate,
    current_user: UserInDB = Depends(get_current_active_admin_user),
    db: Any = Depends(get_db_session)
):
    gym_data_dict = gym_data.model_dump()
    gym_data_dict["owner_id"] = current_user.id

    # Re-create GymCreate with the enforced owner_id
    gym_to_create = GymCreate(**gym_data_dict)

    try:
        created_gym = create_gym(db=db, gym_data=gym_to_create)
        # Convert GymInDB to GymPublic if they are different, or ensure model compatibility
        # For now, assuming GymInDB can be returned if GymPublic is compatible (e.g. subset or same)
        # The models defined (GymInDB contains id, GymPublic is a subset) work well if GymPublic is response_model
        return created_gym # FastAPI will handle response_model conversion
    except ValueError as e: # Catching potential ValueError from create_gym if owner_id is not set
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Consider logging the exception e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred while creating the gym.")

@router.get(
    "/gyms/{gym_id}",
    response_model=GymPublic,
    summary="Get Gym Details",
    description="Retrieves the details for a specific gym by its ID. Requires admin privileges."
)
async def get_single_gym(
    gym_id: str = Path(..., description="The ID of the gym to retrieve."),
    current_user: UserInDB = Depends(get_current_active_admin_user), # Enforce admin access
    db: Any = Depends(get_db_session)
):
    gym = get_gym_by_id(db=db, gym_id=gym_id)
    if not gym:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found.")
    return gym

@router.put(
    "/gyms/{gym_id}",
    response_model=GymPublic,
    summary="Update Gym Details",
    description="Allows the admin owner of a gym to update its details. Partial updates are supported."
)
async def update_existing_gym(
    gym_update_data: GymUpdate,
    gym: GymInDB = Depends(get_gym_owner_verified),
    db: Any = Depends(get_db_session)
):
    # The gym_owner_verified dependency handles:
    # 1. Authentication of current_user as active admin.
    # 2. Retrieval of gym by gym_id.
    # 3. Verification that current_user.id == gym.owner_id.
    # It returns the gym object if all checks pass.

    # GymUpdate model should not include 'owner_id' to prevent accidental changes.
    # If 'owner_id' was part of GymUpdate and different from gym.owner_id, a check would be needed:
    # if gym_update_data.owner_id and gym_update_data.owner_id != gym.owner_id:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot change gym ownership via this endpoint.")

    updated_gym = update_gym_details(db=db, gym_id=gym.id, gym_update_data=gym_update_data)
    if not updated_gym:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found or update failed.")
    return updated_gym

@router.delete(
    "/gyms/{gym_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Gym",
    description="Allows the admin owner of a gym to delete it. This operation is irreversible."
)
async def delete_existing_gym(
    gym: GymInDB = Depends(get_gym_owner_verified),
    db: Any = Depends(get_db_session)
):
    deleted = delete_gym_by_id(db=db, gym_id=gym.id)
    if not deleted:
        # This might occur if the gym was deleted between the check and the delete operation (race condition)
        # or if delete_gym_by_id itself has conditions for failure not covered by gym existence.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found or could not be deleted.")
    return None


@router.get(
    "/gyms/{gym_id}/subscribers",
    response_model=List[SubscribedUserDetail],
    summary="List Gym Subscribers",
    description="Retrieves a list of all users subscribed to a specific gym. Only accessible by the gym owner admin. Includes subscription details and latest physical data of users."
)
async def get_gym_subscribers(
    gym: GymInDB = Depends(get_gym_owner_verified),
    db: Any = Depends(get_db_session)
):
    subscriptions = get_subscriptions_by_gym_id(db=db, gym_id=gym.id)
    if not subscriptions:
        return []

    subscribed_user_details: List[SubscribedUserDetail] = []
    for sub in subscriptions:
        user = get_user_by_id(db=db, user_id=sub.user_id) # Updated function call
        if user:
            latest_physical_data = None
            if user.physical_data_history:
                # Sort by record_date to get the latest, assuming record_date is datetime
                # Pydantic models from model_dump in database.py might be dicts, need to ensure they are objects
                # or handle dict access. Assuming they are Pydantic objects here.
                # If physical_data_history stores Pydantic models:
                # user.physical_data_history.sort(key=lambda pd: pd.record_date, reverse=True)
                # latest_physical_data = user.physical_data_history[0]
                # If physical_data_history stores dicts (due to model_dump in create_user):
                if isinstance(user.physical_data_history[0], dict):
                    # Sort list of dicts by 'record_date'
                    sorted_history = sorted(user.physical_data_history, key=lambda pd: pd['record_date'], reverse=True)
                    latest_physical_data = PhysicalDataBase(**sorted_history[0])
                elif isinstance(user.physical_data_history[0], PhysicalDataBase):
                     # Sort list of Pydantic objects by 'record_date'
                    user.physical_data_history.sort(key=lambda pd: pd.record_date, reverse=True)
                    latest_physical_data = user.physical_data_history[0]


            detail = SubscribedUserDetail(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                address=user.address,
                plan_name=sub.plan_name,
                subscription_start_date=sub.start_date,
                subscription_end_date=sub.end_date,
                subscription_is_active=sub.is_active,
                training_type_opted=sub.training_type_opted,
                latest_physical_data=latest_physical_data
            )
            subscribed_user_details.append(detail)
        else:
            # Log if a user for a subscription is not found, could indicate data inconsistency
            print(f"Warning: User with ID {sub.user_id} for subscription {sub.id} not found.")

    return subscribed_user_details

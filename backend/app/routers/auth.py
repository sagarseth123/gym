from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
import logging # For logging

# App imports
from app.models.user import UserCreate, UserPublic, UserRole, UserInDB
from app.schemas.user import TokenResponse # Import TokenResponse
from app.auth_utils import hash_password, create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_user_by_email, create_user, get_db

# Placeholder for DB session dependency - replace with actual DB session management
# For now, get_db() is synchronous and might manage a global client,
# or it could be adapted for FastAPI's dependency injection with an async client.
# If get_db is async, endpoints using it must be async too.
# For this subtask, we'll assume get_db() provides what's needed by CRUD functions.
async def get_db_session(): # Placeholder async dependency
    # In a real app, this would yield a database session
    # from a pool or manage a request-scoped session.
    # For now, it calls the synchronous get_db().
    # If your get_db() and CRUD are async, this would be different.
    try:
        db = get_db() # This is the synchronous get_db from database.py
        return db
    except Exception as e:
        logging.error(f"Database connection error in get_db_session: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection failed.")


router = APIRouter()

@router.post(
    "/signup/admin",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Admin User Signup",
    description="Allows a new user to sign up with administrative privileges. The user's password will be hashed before storage."
)
async def signup_admin(user: UserCreate, db: Any = Depends(get_db_session)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    if not user.hashed_password: # Password should be provided in UserCreate for signup
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password not provided."
        )

    hashed_pw = hash_password(user.hashed_password) # Hash the provided password

    # Create a new UserCreate instance with the hashed password
    # and other details for creation.
    # The role will be set by create_user function or by preparing the model.
    user_to_create = UserCreate(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pw, # Store the hashed password
        google_id=user.google_id,
        role=UserRole.admin, # Explicitly set role here for clarity before passing to create_user
        is_active=user.is_active,
        # address and physical_data_history are optional and can be omitted or passed
        address=user.address
    )

    try:
        created_user = create_user(db=db, user_create_data=user_to_create, role=UserRole.admin)
        # UserPublic model will be used by FastAPI based on response_model
        return created_user
    except ValueError as e:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(f"Error during admin user creation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating admin user.")


@router.post(
    "/login/admin",
    response_model=TokenResponse,
    summary="Admin User Login",
    description="Authenticates an admin user based on email and password, returning a JWT access token if successful."
)
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Any = Depends(get_db_session)):
    user = get_user_by_email(db=db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for admin access.",
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value} # 'sub' is a standard claim for subject (user identifier)
    )
    return TokenResponse(access_token=access_token, token_type="bearer")

# --- Google OAuth Stubs ---

@router.get(
    "/google/login",
    summary="Initiate Google OAuth Login (Stub)",
    description="Placeholder endpoint to simulate the start of a Google OAuth2 login flow. In a real application, this would redirect the user to Google's authentication server."
)
async def google_login():
    # Example redirect (actual implementation would use configuration for client_id, redirect_uri etc.)
    # from starlette.responses import RedirectResponse
    # google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    # params = {
    #     "client_id": "YOUR_GOOGLE_CLIENT_ID",
    #     "redirect_uri": "YOUR_REDIRECT_URI", # e.g., http://localhost:8000/auth/google/callback
    #     "response_type": "code",
    #     "scope": "openid email profile",
    #     "access_type": "offline", # if you need refresh tokens
    # }
    # from urllib.parse import urlencode
    # return RedirectResponse(f"{google_auth_url}?{urlencode(params)}")
    return {"message": "Google login initiated. Redirect to Google OAuth flow here. (This is a stub)"}

@router.get(
    "/google/callback",
    summary="Handle Google OAuth Callback (Stub)",
    description="Placeholder endpoint to simulate handling the callback from Google after user authentication. In a real application, this endpoint would receive an authorization code, exchange it for tokens, and then create or log in the user."
)
async def google_callback(code: str = None, error: str = None, db: Any = Depends(get_db_session)):
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Google OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing authorization code from Google.")

    # 1. Exchange code for tokens (POST request to Google's token endpoint)
    #    - Requires client_id, client_secret, code, redirect_uri, grant_type="authorization_code"
    #    - Example: token_response = httpx.post("https://oauth2.googleapis.com/token", data=...)
    #    - access_token = token_response.json().get("access_token")
    #    - id_token = token_response.json().get("id_token") (JWT containing user info)

    # 2. (Optional) Verify id_token or use access_token to get user info
    #    - User info from id_token: decoded_id_token = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": False}) # Or verify with Google's public keys
    #    - User info from API: user_info_response = httpx.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    #    - email = user_info_response.json().get("email")
    #    - google_id = user_info_response.json().get("id")
    #    - full_name = user_info_response.json().get("name")

    # For placeholder:
    mock_email = f"user_{code}@example.com" # Simulate email from Google
    mock_google_id = f"google_id_{code}"
    mock_full_name = "Google User"

    # 3. Find or create user in your database
    user = get_user_by_email(db=db, email=mock_email)
    if not user:
        # Create new user (password can be None or a securely generated random string if local login is disabled)
        # For this example, we'll assume users created via Google might not have a local password.
        new_user_data = UserCreate(
            email=mock_email,
            full_name=mock_full_name,
            hashed_password=None, # Or generate one if needed for some reason
            google_id=mock_google_id,
            role=UserRole.user, # Default role for Google signups
            is_active=True
        )
        # Ensure role is passed as UserRole enum or string value
        user = create_user(db=db, user_create_data=new_user_data, role=UserRole.user)

    # 4. Create access token for your application
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value, "google_id": user.google_id if user.google_id else None}
    )
    return TokenResponse(access_token=access_token, token_type="bearer") # Also return TokenResponse here
    # Can add more fields to response like: "email": user.email, "message": "Google login/signup successful."
    # but TokenResponse is the primary contract for token endpoints.

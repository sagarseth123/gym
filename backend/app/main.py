from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import auth, gym_admin

# Define allowed origins for CORS
origins = [
    "http://localhost:3000",  # Default for Create React App
    # "http://localhost:3001", # Another example if your frontend runs elsewhere
    # "https://your-deployed-frontend.com", # Example for production
]

app = FastAPI(
    title="Gym Management API",
    version="0.1.0",
    description="""
Welcome to the **Gym Management API**!

This API provides a comprehensive solution for managing gyms, users, subscriptions, and related activities.
It features robust authentication and role-based access control.

**Key Features:**
- User Authentication (Admin Signup, Login, Google OAuth Stubs)
- Admin-only Gym Management (CRUD operations for gyms)
- Subscription Management (View subscribers for a gym)
- User Profile and Physical Data Tracking (Implicit through models)

Built with FastAPI and MongoDB.
    """
)

# Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Allows cookies / auth headers, important for some auth flows
    allow_methods=["*"],    # Allows all standard methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allows all headers
)

@app.on_event("startup")
async def startup_db_client():
    print("FastAPI application startup: Attempting to connect to MongoDB...")
    connect_to_mongo() # Call the updated connection function

@app.on_event("shutdown")
async def shutdown_db_client():
    print("FastAPI application shutdown: Closing MongoDB connection...")
    close_mongo_connection() # Call the close connection function


@app.get("/")
async def root():
    return {"message": "Welcome to the Gym Management API!"}

# Include the authentication router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include the gym admin router
app.include_router(gym_admin.router, prefix="/admin", tags=["Gym Management (Admin)"])

# You can re-add your example router if you want
# from .routers import example
# app.include_router(example.router)

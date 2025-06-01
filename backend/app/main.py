from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection # Updated import
from app.routers import auth, gym_admin # Import the auth and gym_admin routers

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

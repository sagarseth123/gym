from fastapi import FastAPI
from .database import connect_and_ping_db # Import the function

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    print("FastAPI application startup...")
    connect_and_ping_db() # Call the connection function

@app.on_event("shutdown")
async def shutdown_db_client():
    # If you need to explicitly close the client or do other cleanup
    # from .database import client
    # if client:
    #    client.close()
    #    print("MongoDB connection closed.")
    print("FastAPI application shutdown...")


@app.get("/")
async def root():
    return {"message": "Hello World - FastAPI connected to MongoDB (hopefully!)"}

# You can re-add your example router if you want
# from .routers import example
# app.include_router(example.router)

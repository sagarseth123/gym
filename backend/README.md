# Backend (FastAPI)

This directory contains the FastAPI application for the Gym Management Platform.

## Setup and Running

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure MongoDB:**
    - Ensure you have a MongoDB instance running.
    - Update the `MONGO_DETAILS` in `app/database.py` with your MongoDB connection string and desired database name.
      (Ideally, this will be moved to environment variables later).

4.  **Run the application:**
    Navigate to the `backend/app` directory (where `main.py` is located).
    ```bash
    cd app
    uvicorn main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`. You can access the API docs at `http://127.0.0.1:8000/docs`.

## Project Structure
- `app/main.py`: The main FastAPI application instance.
- `app/database.py`: Handles MongoDB connection and database access.
- `app/models/`: Contains Pydantic models for database objects (e.g., User, Gym).
- `app/schemas/`: Contains Pydantic schemas for request/response validation and serialization. (Note: currently, Pydantic models in `app/models` serve both purposes, this can be split further if needed).
- `app/routers/`: Contains API route definitions.
- `requirements.txt`: Lists Python dependencies.

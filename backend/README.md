# Backend (FastAPI)

This directory contains the FastAPI application for the Gym Management Platform.

## Setup and Running

1.  **Navigate to the `backend` directory (if you are not already there):**
    ```bash
    cd path/to/your_project/backend
    ```
    *(Ensure your terminal's current working directory is the `backend` folder that contains `app` and `requirements.txt`)*

2.  **Create a virtual environment (recommended, if not already done):**
    From within the `backend` directory:
    ```bash
    python3 -m venv venv  # Or python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies (if not already done):**
    From within the `backend` directory (with virtual environment activated):
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure MongoDB:**
    - Ensure you have a MongoDB instance running.
    - **Crucially, ensure `MONGO_DETAILS` and `DB_NAME` in `app/database.py` are correctly set to your MongoDB connection string and desired database name.** You can edit the file directly or set them as environment variables (e.g., `export MONGO_DETAILS="your_uri"` `export DB_NAME="your_db"`) before running the server. Remember to replace placeholder values.

5.  **Run the application:**
    From within the `backend` directory (with virtual environment activated):
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    This command tells Python to run Uvicorn as a module, looking for the `app` object within the `app.main` module (i.e., `backend/app/main.py`).

    The application will be available at `http://127.0.0.1:8000`. You can access the API docs at `http://127.0.0.1:8000/docs`.

## Project Structure
- `app/main.py`: The main FastAPI application instance.
- `app/database.py`: Handles MongoDB connection and database access.
- `app/models/`: Contains Pydantic models for database objects (e.g., User, Gym).
- `app/schemas/`: Contains Pydantic schemas for request/response validation and serialization. (Note: currently, Pydantic models in `app/models` serve both purposes, this can be split further if needed).
- `app/routers/`: Contains API route definitions.
- `requirements.txt`: Lists Python dependencies.

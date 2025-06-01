# Gym Management Platform

This project is a comprehensive gym management platform with features for both gym administrators and gym users.

**Tech Stack:**
- **Frontend:** React
- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **Authentication:** Google & Local

## Project Structure
- `/frontend`: Contains the React frontend application.
- `/backend`: Contains the FastAPI backend application.
- `/database`: Contains database-related scripts and configurations (currently, connection logic is in `backend/app/database.py`).

## How to Run Locally

This section provides instructions on how to get the project running on your local machine for development and testing purposes.

### Backend (FastAPI)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure MongoDB:**
    - Ensure you have a MongoDB instance running.
    - Update the `MONGO_DETAILS` in `app/database.py` with your MongoDB connection string and desired database name.
      (Note: This will ideally be moved to environment variables in future development).
5.  **Run the application:**
    Navigate to the `app` directory (where `main.py` is located) from within the `backend` directory.
    ```bash
    cd app
    uvicorn main:app --reload
    ```
    The backend server will start, typically at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

For more details, refer to the `backend/README.md`.

### Frontend (React)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    If this is the first time or dependencies have changed:
    ```bash
    npm install
    ```
3.  **Run the application:**
    ```bash
    npm start
    ```
    This runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser. The page will automatically reload if you make changes to the code.

For more details on other available scripts (`npm test`, `npm run build`), refer to the `frontend/README.md`.

## Getting Started (Development Workflow)
(Instructions to be added as development progresses for overall workflow)

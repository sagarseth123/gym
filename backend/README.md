# Gym Administration Backend

This backend system is built using FastAPI and MongoDB to provide administrative functionalities for gym owners on the platform.

## Table of Contents
- [Overall Architecture](#overall-architecture)
- [Module Overview](#module-overview)
- [Authentication Flow](#authentication-flow)
  - [Admin Signup](#admin-signup)
  - [Admin Login](#admin-login)
- [API Endpoints](#api-endpoints)
  - [Authentication (`/auth`)](#authentication-auth)
  - [Gym Management (`/admin/gyms`)](#gym-management-admingyms)
- [Database Schema](#database-schema)
  - [`users` collection](#users-collection)
  - [`gyms` collection](#gyms-collection)
  - [`subscriptions` collection](#subscriptions-collection)
- [Setup and Running](#setup-and-running)

## Overall Architecture

The backend is a Python application powered by the [FastAPI](https://fastapi.tiangolo.com/) framework, chosen for its high performance and developer-friendly features, including automatic data validation and OpenAPI documentation generation. Data is persisted in a [MongoDB](https://www.mongodb.com/) NoSQL database, providing flexibility for evolving data structures.

## Module Overview

The backend codebase is organized into several key directories and files within the `app/` directory:

-   **`main.py`**: The entry point of the FastAPI application. It initializes the app, includes routers, and handles global configurations like database connections.
-   **`database.py`**: Manages MongoDB connection, provides database session access (`get_db`), and contains CRUD (Create, Read, Update, Delete) functions for interacting with the database collections.
-   **`models/`**: Contains Pydantic models that define the structure of data stored in the database (e.g., `UserInDB`, `GymInDB`). These models often include an `_id` field for MongoDB ObjectId mapping.
    -   `user.py`: User-related models, including roles and physical data.
    -   `gym.py`: Gym-related models, including equipment, trainers, subscription plans.
    -   `subscription.py`: Subscription linking users to gyms and plans.
    -   `physical_data.py`: Model for user's physical measurements.
-   **`schemas/`**: Contains Pydantic models used for API request and response validation (e.g., `UserCreate`, `GymPublic`, `SubscribedUserDetail`). These shape the data exchanged via the API.
    -   `user.py`: Schemas for user-related API operations, like `SubscribedUserDetail` and `TokenResponse`.
-   **`routers/`**: Defines API endpoints. Each file typically groups related endpoints.
    -   `auth.py`: Handles authentication routes like admin signup and login (local and Google OAuth stubs).
    -   `gym_admin.py`: Manages administrative routes for gym creation, updates, deletion, and viewing subscribers.
-   **`dependencies.py`**: Implements FastAPI dependencies used for request validation, authentication, and authorization (e.g., `get_current_active_admin_user`, `get_gym_owner_verified`).
-   **`auth_utils.py`**: Provides utility functions for authentication, such as password hashing/verification and JWT token creation/decoding.

## Authentication Flow

### Admin Signup
1.  An admin user signs up via `POST /auth/signup/admin` with email and password.
2.  The system hashes the password and stores the new admin user in the `users` collection with the `admin` role.

### Admin Login
1.  An admin user logs in via `POST /auth/login/admin` using their email and password.
2.  The system verifies the credentials against the stored hashed password.
3.  Upon successful authentication, a JWT (JSON Web Token) access token is generated and returned to the client.
4.  This token must be included in the `Authorization` header (as a Bearer token) for accessing protected endpoints.

## API Endpoints

### Authentication (`/auth`)

-   **`POST /signup/admin`**: Registers a new gym administrator.
    -   Request Body: `UserCreate` schema (email, password, full_name).
    -   Response: `UserPublic` schema.
-   **`POST /login/admin`**: Logs in an existing gym administrator.
    -   Request Body: Form data (username = email, password).
    -   Response: `TokenResponse` schema (access_token, token_type).
-   **`GET /google/login`**: (Stub) Initiates Google OAuth2 login flow.
-   **`GET /google/callback`**: (Stub) Handles Google OAuth2 callback.

### Gym Management (`/admin/gyms`)

All endpoints under `/admin/gyms` require authentication as an admin user. Update and delete operations further require the authenticated admin to be the owner of the gym.

-   **`POST /gyms`**: Creates a new gym.
    -   Request Body: `GymCreate` schema.
    -   Response: `GymPublic` schema.
    -   The `owner_id` is automatically set to the authenticated admin's ID.
-   **`GET /gyms/{gym_id}`**: Retrieves details for a specific gym.
    -   Response: `GymPublic` schema.
-   **`PUT /gyms/{gym_id}`**: Updates details for a specific gym.
    -   Request Body: `GymUpdate` schema (allows partial updates).
    -   Response: `GymPublic` schema.
    -   Requires ownership.
-   **`DELETE /gyms/{gym_id}`**: Deletes a specific gym.
    -   Response: HTTP 204 No Content.
    -   Requires ownership.
-   **`GET /gyms/{gym_id}/subscribers`**: Retrieves a list of subscribers for a specific gym.
    -   Response: List of `SubscribedUserDetail` schemas.
    -   Requires ownership.

## Database Schema

The application uses MongoDB. Key collections include:

### `users` collection
Stores information about all users (gym admins and regular users).
-   `_id`: ObjectId (Primary Key)
-   `email`: String (Unique, Indexed)
-   `full_name`: String (Optional)
-   `hashed_password`: String (For local authentication)
-   `google_id`: String (Optional, for Google OAuth)
-   `role`: String (Enum: "admin", "user")
-   `is_active`: Boolean
-   `address`: String (Optional)
-   `physical_data_history`: Array of embedded `PhysicalData` objects:
    -   `weight_kg`: Float
    -   `height_cm`: Float
    -   `bmi`: Float
    -   `record_date`: DateTime
-   `created_at`: DateTime
-   `updated_at`: DateTime

### `gyms` collection
Stores details about the gyms registered on the platform.
-   `_id`: ObjectId (Primary Key)
-   `name`: String
-   `owner_id`: String (References `_id` in `users` collection, Indexed)
-   `area_sq_ft`: Float (Optional)
-   `address`: String (Optional)
-   `equipments`: Array of embedded `Equipment` objects:
    -   `name`: String
    -   `quantity`: Integer
-   `personal_trainers`: Array of embedded `Trainer` objects:
    -   `name`: String
    -   `specialization`: String
    -   `fee`: Float
-   `subscription_plans`: Array of embedded `SubscriptionPlan` objects:
    -   `name`: String
    -   `duration_days`: Integer
    -   `price`: Float
    -   `features`: List of Strings
-   `training_types_offered`: Array of embedded `TrainingType` objects:
    -   `name`: String
    -   `description`: String (Optional)
-   `is_verified`: Boolean (Default: false)
-   `created_at`: DateTime
-   `updated_at`: DateTime

### `subscriptions` collection
Links users to the gyms they have subscribed to and the specific plan.
-   `_id`: ObjectId (Primary Key)
-   `user_id`: String (References `_id` in `users` collection, Indexed)
-   `gym_id`: String (References `_id` in `gyms` collection, Indexed)
-   `plan_name`: String (Could also be a plan_id if plans become a separate collection)
-   `start_date`: DateTime
-   `end_date`: DateTime
-   `is_active`: Boolean
-   `training_type_opted`: String (Optional)
-   `created_at`: DateTime
-   `updated_at`: DateTime

## Setup and Running

1.  **Prerequisites**:
    -   Python 3.8+
    -   MongoDB instance running.
2.  **Installation**:
    -   Clone the repository.
    -   Navigate to the `backend` directory.
    -   Create a virtual environment: `python -m venv venv`
    -   Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
    -   Install dependencies: `pip install -r requirements.txt`
3.  **Configuration**:
    -   Set environment variables for MongoDB connection if customized in `app/database.py` (e.g., `MONGO_URI`, `MONGO_DB_NAME`).
4.  **Running the application**:
    -   From the `backend` directory: `uvicorn app.main:app --reload`
5.  **API Documentation**:
    -   Once running, access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.
    -   Access ReDoc documentation at `http://localhost:8000/redoc`.

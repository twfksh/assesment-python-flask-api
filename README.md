# Flask Auth API

A simple authentication API built with Flask, SQLModel, and JWT. This project provides user registration, login, token-based authentication, and user management endpoints.

## Features

- User registration and login with hashed passwords
- JWT-based authentication (access and refresh tokens)
- Token revocation (logout)
- User listing and retrieval
- Pydantic validation for request data
- SQLModel ORM for database access with validation

## Project Structure

- [`app.py`](app.py): Application entry point and Flask app setup
- [`components.py`](components.py): API route definitions (register, login, logout, user management)
- [`services.py`](services.py): Business logic for authentication and user management
- [`models.py`](models.py): SQLModel database models (`User`, `TokenBlocklist`)
- [`schemas.py`](schemas.py): Pydantic schemas for request validation
- [`database.py`](database.py): Database engine and initialization
- `.env.sample`: Example environment variables

## Setup

1. **Clone the repository**
    ```sh
    git clone https://github.com/twfksh/assesment-python-flask-api
    cd assesment-python-flask-api
    ```

2. **Install dependencies**

   ```sh
   uv venv
   uv pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Copy `.env.sample` to `.env` and fill in the required values:

   ```
   cp .env.sample .env
   ```

   Set at least:
   - `SQLMODEL_DATABASE_URL`
   - `FLASK_SECRET_KEY`
   - `FLASK_JWT_SECRET_KEY`

4. **Initialize the database**

   The database tables are created automatically on app startup.

5. **Run the application**

   ```sh
   uv run flask run
   ```

## API Endpoints

### Auth

- `POST /api/auth/register`  
  Register a new user.  
  **Body:** `{ "username": "user", "password": "password" }`

- `POST /api/auth/login`  
  Login and receive access/refresh tokens.  
  **Body:** `{ "username": "user", "password": "password" }`

- `GET /api/auth/whoami`  
  Get current user info (JWT required).

- `GET /api/auth/refresh`  
  Refresh access token (refresh JWT required).

- `GET /api/auth/logout`  
  Logout and revoke the current token.

### Users

- `GET /api/users/all`  
  List all users (JWT required).

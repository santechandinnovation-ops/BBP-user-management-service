# BBP User Management Service

Microservice for authentication and user profile management.

## Overview

Handles user registration, authentication, and profile management. Uses JWT tokens for stateless authentication and PostgreSQL for user data storage. Passwords are securely hashed using bcrypt.

## Features

- **User Registration**: Create new accounts with validation
- **Authentication**: Login/logout with JWT tokens
- **Profile Management**: View and update user profiles
- **Password Security**: Bcrypt hashing with salt
- **Token Management**: JWT with configurable expiration

## Tech Stack

- FastAPI
- PostgreSQL (psycopg2)
- Python-Jose (JWT)
- Passlib + Bcrypt (password hashing)
- Pydantic (validation)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | User login |
| POST | `/auth/logout` | User logout |
| GET | `/users/profile` | Get current user profile |
| PUT | `/users/profile` | Update profile |
| GET | `/users/{id}` | Get user by ID |

## Database Tables

- `users` - User accounts and profiles

## Environment Variables

```
DATABASE_URL=<postgresql-url>
JWT_SECRET_KEY=<secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## Running Locally

```bash
pip install -r requirements.txt
python database/setup_db.py  # Initialize tables
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Deployment

Deployed on Railway. See `Procfile` for startup command.

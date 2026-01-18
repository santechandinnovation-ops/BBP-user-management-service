# BBP User Management Service

Authentication and user management microservice for the Best Bike Paths (BBP) application.

## Features

- User registration with email uniqueness validation
- Password strength validation (min 8 chars, 1 uppercase, 1 number)
- Secure password hashing with bcrypt
- JWT token-based authentication
- User profile management
- Health check endpoint

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "username": "string (3-50 characters)",
  "email": "string (valid email format)",
  "password": "string (min 8 characters, 1 uppercase, 1 number)"
}
```

**Response 201:**
```json
{
  "success": true,
  "userId": "uuid",
  "message": "Registration successful"
}
```

#### POST /auth/login
Authenticate user and receive JWT token.

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response 200:**
```json
{
  "success": true,
  "token": "JWT token string",
  "user": {
    "userId": "uuid",
    "username": "string",
    "email": "string"
  }
}
```

#### POST /auth/logout
Invalidate current user session.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

### User Profile

#### GET /users/profile
Retrieve authenticated user profile information.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "userId": "uuid",
  "username": "string",
  "email": "string",
  "registrationDate": "datetime",
  "lastLogin": "datetime"
}
```

### Health Check

#### GET /health
Check service health and database connectivity.

**Response 200:**
```json
{
  "status": "healthy",
  "service": "User Management Service",
  "timestamp": "datetime",
  "database": "connected"
}
```

## Setup Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL database (Supabase)

### Installation

1. Clone the repository and navigate to the service directory:
```bash
cd user-management-service
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

5. Initialize database:
```bash
python database/setup_db.py
```

6. Run the service:
```bash
uvicorn app.main:app --reload --port 8000
```

The service will be available at `http://localhost:8000`

API documentation (Swagger UI) available at `http://localhost:8000/docs`

## Environment Variables

Required environment variables in `.env` file:

- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:password@host:port/database`)
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `JWT_EXPIRATION_HOURS`: Token expiration time (default: 24)
- `PORT`: Service port (default: 8000)

## Deployment to Railway

1. Create new project on Railway
2. Connect your Git repository
3. Set environment variables in Railway dashboard
4. Railway will automatically detect `Procfile` and deploy

Required environment variables for Railway:
- `DATABASE_URL`: Railway will provide this automatically if you add a PostgreSQL database
- `JWT_SECRET_KEY`: Generate a secure random key for production

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

## Testing

### Example cURL Commands

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test1234"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234"}'
```

**Get Profile:**
```bash
curl -X GET http://localhost:8000/users/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

## Technology Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (Supabase)
- **Authentication:** JWT with python-jose
- **Password Hashing:** bcrypt via passlib
- **Validation:** Pydantic
- **Database Driver:** psycopg2

## Security Features

- Bcrypt password hashing with 12 rounds
- JWT tokens with 24-hour expiration
- Email uniqueness validation
- Password strength requirements
- SQL injection prevention via parameterized queries
- CORS middleware for cross-origin requests

# FastAPI Authentication & User Management System

## Overview

This project is a FastAPI-based Authentication and User Management System that provides secure user registration, login, JWT authentication, refresh token functionality, protected routes, and CRUD operations.

The application uses PostgreSQL as the database, SQLAlchemy as the ORM, and JWT for secure authentication.

---

## Features

* User Registration
* User Login
* Password Hashing using bcrypt
* JWT Access Token Authentication
* Refresh Token Support
* Protected Routes
* User Profile API
* User CRUD Operations
* PostgreSQL Integration
* SQLAlchemy ORM
* Swagger API Documentation

---

## Tech Stack

### Backend

* FastAPI
* Python 3.10+

### Database

* PostgreSQL

### ORM

* SQLAlchemy

### Authentication

* JWT (JSON Web Token)
* Passlib (bcrypt)

### API Documentation

* Swagger UI
* ReDoc

---

## Project Structure

```text
fastapi-auth-api/
│
├── app/
│   ├── database/
│   │   ├── db.py
|   |   ├── base.py
│   │
│   ├── models/
│   │   ├── user.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   
│   │
│   ├── schemas/
│   │   ├── user.py
│   │
│   ├── services/
│   │   ├── security.py
│   │   ├── jwt_handler.py
│   │
│   └── main.py
│
├── tests/
│
├── .env
├── requirements.txt
├── README.md
│
└── venv/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/MohanlalSathyamurthy/fastapi-auth-api.git
cd fastapi-auth-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

Linux/Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=15

REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Authentication Flow

```text
User Registration
        ↓
Store User in PostgreSQL
        ↓
Password Hashed with bcrypt
        ↓
User Login
        ↓
Generate Access Token
Generate Refresh Token
        ↓
Protected APIs
        ↓
Validate JWT Token
```

---

## API Endpoints

### Authentication

#### Register User

```http
POST /register
```

#### Login User

```http
POST /login
```

#### Refresh Token

```http
POST /refresh
```

#### Logout

```http
POST /logout
```

---

### User APIs

#### Get Profile

```http
GET /profile
```

#### Get All Users

```http
GET /users
```

#### Get User By ID

```http
GET /user/{user_id}
```

#### Update User

```http
PUT /user/{user_id}
```

#### Delete User

```http
DELETE /user/{user_id}
```

---

## Security Features

* Password Hashing using bcrypt
* JWT Authentication
* Refresh Token Support
* Protected Routes
* Token Validation
* Secure Password Storage

---

## Sample Login Response

```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "bearer"
}
```
## Docker Setup

* Build Docker Image
docker build -t fastapi-auth-api .

* Run Docker Container
docker run --network host --env-file .env fastapi-auth-api

* The application will be available at:
http://localhost:8000

* Swagger Documentation:
http://localhost:8000/docs


---

## Future Enhancements

* Role-Based Access Control (RBAC)
* Email Verification
* Password Reset
* Docker Support
* Unit Testing
* Pytest Integration
* CI/CD Pipeline
* User Activity Logging

---


## Author

Mohanlal Sathyamurthy

GitHub:
https://github.com/MohanlalSathyamurthy

```
```
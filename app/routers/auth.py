from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, loginUser
from app.services.security import hash_password, verify_password
from app.services.jwt_handler import create_access_token, verify_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create new user instance
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    # Add to database and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        'message': 'User registered successfully',
        'user_id': new_user.id,
    }

@router.post("/login")
def login(user: loginUser, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )
    access_token = create_access_token(data={"sub": existing_user.email, "username": existing_user.username, "created_at": existing_user.created_at.isoformat(), "id": existing_user.id})
    return {
        'token': access_token,
        'token_type': 'bearer'
    }
   
@router.get("/profile")
def get_profile(token_data: dict = Depends(verify_access_token)):
  
    return {
        'id': token_data.get("id"),
        'username': token_data.get("username"),
        'email': token_data.get("sub"),
        'created_at': token_data.get("created_at")
    }

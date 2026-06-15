from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.services.security import hash_password

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
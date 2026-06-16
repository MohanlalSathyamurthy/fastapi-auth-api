from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, loginUser, UserUpdate
from app.services.security import hash_password, verify_password
from app.services.jwt_handler import create_access_token, create_refresh_token, verify_access_token

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
    refresh_token = create_refresh_token(data={"sub": existing_user.email, "username": existing_user.username, "created_at": existing_user.created_at.isoformat(), "id": existing_user.id})
    return {
        'token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }
@router.post("/refresh")
def refresh_token(token_data: dict = Depends(verify_access_token)):
    # Check if the token type is 'refresh'
    if token_data.get("token_type") != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type for refresh token"
        )
    
    # Create a new access token
    new_access_token = create_access_token(data={"sub": token_data.get("sub"), "username": token_data.get("username"), "created_at": token_data.get("created_at"), "id": token_data.get("id")})
    
    return {
        'token': new_access_token
    }

@router.get("/profile")
def get_profile(token_data: dict = Depends(verify_access_token)):
  
    return {
        'id': token_data.get("id"),
        'username': token_data.get("username"),
        'email': token_data.get("sub"),
        'created_at': token_data.get("created_at")
    }
@router.post("/logout")
def logout():
    # Invalidate the token on the client side by instructing the client to delete it.
    # Since JWTs are stateless, we cannot invalidate them server-side without additional mechanisms.
    return {
        'message': 'User logged out successfully.'
    }

@router.get("/all-users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        })
    return result

@router.get("/user/{user_id}", dependencies=[Depends(verify_access_token)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at
    }

@router.delete("/user/{user_id}", dependencies=[Depends(verify_access_token)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return {
        'message': 'User deleted successfully'
    }

@router.put("/user/{user_id}", dependencies=[Depends(verify_access_token)])
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    existing_user = db.query(User).filter(User.email == updated_user.email).first()
    if existing_user and existing_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    # Update user fields
    if updated_user.username:
        user.username = updated_user.username
    if updated_user.email:
        user.email = updated_user.email
    if updated_user.password:
        user.hashed_password = hash_password(updated_user.password)
    db.commit()
    db.refresh(user)
    
    return {
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
    }
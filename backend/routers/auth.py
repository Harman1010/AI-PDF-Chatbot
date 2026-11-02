import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.users import User
from backend.schemas.auth import UserRegister, UserResponse, UserLogin, TokenResponse

from backend.security import hash_password, verify_password, create_access_token

from backend.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)

def register_user(user_data: UserRegister,db: Session = Depends(get_db)):
    # Check whether the email is already registered
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email is already registered.")

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create a new user
    new_user = User(id=str(uuid.uuid4()),email=user_data.email,hashed_password=hashed_password)

    # Save user in database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Could not create user.")

    return new_user

@router.post("/login", response_model=TokenResponse)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    # 1. Find user by email
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    # 2. Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # 3. Verify submitted password against stored hash
    is_valid = verify_password(
        user_data.password,
        user.hashed_password
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # 4. Generate JWT
    token = create_access_token(user.id)

    # 5. Return access token
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
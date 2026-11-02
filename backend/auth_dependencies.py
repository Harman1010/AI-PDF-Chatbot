from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

from backend.database import get_db
from backend.security import verify_access_token
from backend.users import User

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db: Session = Depends(get_db)):

    # Get JWT from request
    token = credentials.credentials

    # Verify JWT
    try:
        payload = verify_access_token(token)

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid or expired token")

    # Get user ID from JWT
    user_id = payload.get("sub")

    # Find user in database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401,detail="User not found")

    return user
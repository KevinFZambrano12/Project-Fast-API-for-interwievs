from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.db.session import get_db
from app.db.models import User, RefreshToken

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))

    db.add(RefreshToken(token=refresh, user_id=user.id))
    db.commit()

    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    stored = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    payload = decode_refresh(refresh_token)
    user_id = payload["sub"]

    new_access = create_access_token(user_id)
    return {"access_token": new_access}

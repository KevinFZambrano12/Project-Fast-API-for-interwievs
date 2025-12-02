from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import decode_access
from app.db.session import get_db
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def require_user(roles: list[str] | None = None):
    def wrapper(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
        try:
            payload = decode_access(token)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).get(payload["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")

        if roles and user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user
    return wrapper

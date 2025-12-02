from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-prod-secret"
REFRESH_SECRET = "your-refresh-secret"
ALGO = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str, expires_minutes=15):
    exp = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode({"sub": sub, "exp": exp}, SECRET_KEY, ALGO)

def create_refresh_token(sub: str, expires_days=7):
    exp = datetime.utcnow() + timedelta(days=expires_days)
    return jwt.encode({"sub": sub, "exp": exp}, REFRESH_SECRET, ALGO)

def decode_access(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGO])

def decode_refresh(token: str):
    return jwt.decode(token, REFRESH_SECRET, algorithms=[ALGO])

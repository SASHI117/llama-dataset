# ===============================
# EXISTING VALIDATORS (UNCHANGED)
# ===============================

VALID_BEHAVIORS = {
    "theoretical",
    "practical",
    "calculation",
    "diagnostic",
    "preventive",
    "safety",
}

def validate_behavior(behavior: str):
    if behavior not in VALID_BEHAVIORS:
        raise ValueError("Invalid behavior type")

def validate_crop(crop: str):
    if not crop or not crop.strip():
        raise ValueError("Invalid crop name")

def validate_qa(question: str, answer: str):
    if not question.strip() or not answer.strip():
        raise ValueError("Question and Answer cannot be empty")


# ===============================
# AUTH HELPERS (FINAL & CORRECT)
# ===============================

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# ===============================
# JWT DEPENDENCY
# ===============================

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

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
# AUTH HELPERS (NEW, SAFE)
# ===============================

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # bcrypt supports max 72 bytes → slice to prevent crash
    return pwd_context.hash(password[:72])

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password[:72], hashed)

def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.nurse import Nurse
from app.schemas.auth import NurseRegister, TokenData

_ALGORITHM = "HS256"
_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8-hour shift

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(nurse: Nurse) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(nurse.id),
        "email": nurse.email,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=_ALGORITHM)


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[_ALGORITHM])
        return TokenData(nurse_id=UUID(payload["sub"]), email=payload["email"])
    except (JWTError, KeyError, ValueError):
        raise ValueError("Invalid or expired token")


def register_nurse(db: Session, data: NurseRegister) -> Nurse:
    existing = db.query(Nurse).filter(Nurse.email == data.email).first()
    if existing:
        raise ValueError("Email already registered")
    nurse = Nurse(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(nurse)
    db.commit()
    db.refresh(nurse)
    return nurse


def authenticate_nurse(db: Session, email: str, password: str) -> Nurse:
    nurse = db.query(Nurse).filter(Nurse.email == email).first()
    if not nurse or not verify_password(password, nurse.hashed_password):
        raise ValueError("Invalid email or password")
    if not nurse.is_active:
        raise ValueError("Account is deactivated")
    return nurse

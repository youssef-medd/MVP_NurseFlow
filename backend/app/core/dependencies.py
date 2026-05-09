from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.nurse import Nurse
from app.services.auth_service import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_nurse(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Nurse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = decode_token(token)
    except ValueError:
        raise credentials_exception

    nurse = db.query(Nurse).filter(Nurse.id == token_data.nurse_id).first()
    if not nurse or not nurse.is_active:
        raise credentials_exception
    return nurse

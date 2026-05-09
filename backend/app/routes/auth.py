from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_nurse
from app.models.nurse import Nurse
from app.schemas.auth import NurseRegister, NurseResponse, Token
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=NurseResponse, status_code=201)
def register(data: NurseRegister, db: Session = Depends(get_db)):
    try:
        nurse = auth_service.register_nurse(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return nurse


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        nurse = auth_service.authenticate_nurse(db, form.username, form.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=auth_service.create_access_token(nurse))


@router.get("/me", response_model=NurseResponse)
def me(current_nurse: Nurse = Depends(get_current_nurse)):
    return current_nurse

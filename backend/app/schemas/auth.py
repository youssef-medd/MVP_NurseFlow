from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class NurseRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class NurseResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    nurse_id: UUID
    email: str

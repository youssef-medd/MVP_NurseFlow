from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    patient_ref: Optional[str] = Field(None, min_length=1, max_length=100)


class SessionResponse(BaseModel):
    id: UUID
    nurse_id: str
    patient_ref: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TranscriptUpdate(BaseModel):
    text: str = Field(..., min_length=1, max_length=100_000)

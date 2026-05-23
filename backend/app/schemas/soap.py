from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SOAPNoteResponse(BaseModel):
    id: UUID
    session_id: UUID
    subjective: Optional[str]
    objective: Optional[str]
    assessment: Optional[str]
    plan: Optional[str]
    generated_at: datetime
    reviewed: bool
    submitted: bool

    class Config:
        from_attributes = True


class SOAPNoteEdit(BaseModel):
    subjective: Optional[str] = Field(None, min_length=1, max_length=10_000)
    objective: Optional[str] = Field(None, min_length=1, max_length=10_000)
    assessment: Optional[str] = Field(None, min_length=1, max_length=10_000)
    plan: Optional[str] = Field(None, min_length=1, max_length=10_000)

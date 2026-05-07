from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


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
    subjective: Optional[str] = None
    objective: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None

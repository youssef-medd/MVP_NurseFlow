import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import enum


class SessionStatus(str, enum.Enum):
    active = "active"
    closed = "closed"


class PatientSession(Base):
    __tablename__ = "patient_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nurse_id = Column(String, nullable=False)
    patient_ref = Column(String, nullable=True)
    status = Column(Enum(SessionStatus), default=SessionStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    raw_transcript = Column(Text, nullable=True)

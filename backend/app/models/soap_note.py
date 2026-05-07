import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class SOAPNote(Base):
    __tablename__ = "soap_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("patient_sessions.id"), nullable=False)
    subjective = Column(Text, nullable=True)
    objective = Column(Text, nullable=True)
    assessment = Column(Text, nullable=True)
    plan = Column(Text, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed = Column(Boolean, default=False, nullable=False)
    submitted = Column(Boolean, default=False, nullable=False)
    nurse_edits = Column(Text, nullable=True)

    session = relationship("PatientSession", backref="soap_notes")

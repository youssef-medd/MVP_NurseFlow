from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.session import PatientSession, SessionStatus
from app.schemas.session import SessionCreate


def create_session(db: Session, data: SessionCreate) -> PatientSession:
    session = PatientSession(nurse_id=data.nurse_id, patient_ref=data.patient_ref)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: UUID) -> PatientSession | None:
    return db.query(PatientSession).filter(PatientSession.id == session_id).first()


def close_session(db: Session, session_id: UUID) -> PatientSession | None:
    session = get_session(db, session_id)
    if session and session.status == SessionStatus.active:
        session.status = SessionStatus.closed
        session.closed_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
    return session


def append_transcript(db: Session, session_id: UUID, text: str) -> PatientSession | None:
    session = get_session(db, session_id)
    if not session:
        return None
    session.raw_transcript = (session.raw_transcript or "") + "\n" + text
    db.commit()
    db.refresh(session)
    return session

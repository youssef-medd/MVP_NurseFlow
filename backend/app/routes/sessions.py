from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.session import SessionCreate, SessionResponse, TranscriptUpdate
from app.services import session_service

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=201)
def create_session(data: SessionCreate, db: Session = Depends(get_db)):
    return session_service.create_session(db, data)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: UUID, db: Session = Depends(get_db)):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/{session_id}", response_model=SessionResponse)
def close_session(session_id: UUID, db: Session = Depends(get_db)):
    session = session_service.close_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/{session_id}/transcript")
def append_transcript(session_id: UUID, body: TranscriptUpdate, db: Session = Depends(get_db)):
    session = session_service.append_transcript(db, session_id, body.text)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "ok", "session_id": str(session_id)}


@router.get("/{session_id}/transcript")
def get_transcript(session_id: UUID, db: Session = Depends(get_db)):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": str(session_id), "transcript": session.raw_transcript or ""}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth, soap, sessions

app = FastAPI(
    title="NurseFlow API",
    description="AI-powered clinical workflow assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(soap.router, prefix="/api/v1/sessions", tags=["soap"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "nurseflow-api"}

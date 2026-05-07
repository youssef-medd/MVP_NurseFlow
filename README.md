# NurseFlow

![NurseFlow](./pics/nurseflow-hero.png)

> An AI-powered clinical workflow assistant that listens, understands, and acts — so nurses can stop typing and start nursing.

![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-MVP-orange)
![Stack](https://img.shields.io/badge/stack-Next.js%20%7C%20FastAPI%20%7C%20Claude-blueviolet)

---

## What is NurseFlow?

NurseFlow is an AI admin layer built for clinical environments. It sits between the nurse and the EHR — listening to patient interactions in real time, generating structured SOAP notes automatically, and routing documentation tasks without manual entry.

**The problem it solves:** Nurses spend up to 70% of their shift on paperwork. NurseFlow cuts that down by handling transcription, note generation, and workflow management autonomously.

**Key capabilities (MVP):**
- Real-time audio transcription using Whisper
- Automatic SOAP note generation via Claude AI
- Nurse review dashboard for approval and edits
- Session-based architecture for multi-patient workflows
- Future-ready EHR integration layer

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, TailwindCSS |
| Backend | FastAPI, Python 3.11+ |
| Database | PostgreSQL |
| Transcription | OpenAI Whisper |
| AI / NLP | Claude (Anthropic) |
| Auth | JWT + session tokens |
| Deployment | Docker (local), Vercel + Railway (cloud) |

---

## System Architecture

![NurseFlow System Architecture](./pics/nurseflow-hero.png)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INPUT PIPELINE                               │
│                                                                     │
│  Mic Array → VAD/Vite → Whisper Med → Distillation → Anonymizer    │
│                                              ↓                      │
│                                        Edge Buffer                  │
└──────────────────────────────┬──────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          CORE LAYER                                 │
│                                                                     │
│  API Gateway → Session Manager → AI Engine → EHR Connector         │
│                                     ↓              ↓               │
│                               Audit Logger   Insurance Dir          │
└──────────────────────────────┬──────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        NURSE INTERFACE                              │
│                                                                     │
│  Dashboard  →  SOAP Review  →  Approve / Edit  →  Submit to EHR   │
└─────────────────────────────────────────────────────────────────────┘
```

**Component breakdown:**

| Component | Role |
|-----------|------|
| VAD / Vite | Voice Activity Detection — starts/stops recording per utterance |
| Whisper Med | Medical-domain fine-tuned transcription model |
| Distillation | Cleans and normalizes raw transcript |
| Anonymizer | Strips PII before sending to cloud AI |
| Edge Buffer | Queues audio chunks for reliable delivery |
| API Gateway | Entry point for all client requests |
| Session Manager | Tracks active patient sessions and context |
| AI Engine | Claude-powered SOAP note generation |
| EHR Connector | Adapter layer for future EHR integrations |
| Audit Logger | Immutable log of all AI decisions and nurse actions |

---

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Docker (optional but recommended)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/nurseflow.git
cd nurseflow
```

### 2. Set up the frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### 3. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### 4. Set up the database

```bash
psql -U postgres -c "CREATE DATABASE nurseflow;"
# Run migrations (once implemented)
alembic upgrade head
```

Frontend runs at `http://localhost:3000`, backend at `http://localhost:8000`.

---

## Environment Variables

### Frontend (`frontend/.env.local`)

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL for real-time transcription |

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `ANTHROPIC_API_KEY` | Claude API key from console.anthropic.com |
| `OPENAI_API_KEY` | Whisper transcription API key |
| `JWT_SECRET` | Secret key for signing session tokens |
| `ENVIRONMENT` | `development` or `production` |

---

## API Overview

All endpoints are prefixed with `/api/v1`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/sessions` | Start a new patient session |
| `GET` | `/sessions/:id` | Get session details and status |
| `DELETE` | `/sessions/:id` | End and close a session |
| `POST` | `/sessions/:id/audio` | Upload an audio chunk for transcription |
| `GET` | `/sessions/:id/transcript` | Get the current live transcript |
| `POST` | `/sessions/:id/soap` | Trigger SOAP note generation |
| `GET` | `/sessions/:id/soap` | Retrieve the generated SOAP note |
| `PATCH` | `/sessions/:id/soap` | Save nurse edits to the SOAP note |
| `POST` | `/sessions/:id/submit` | Mark note as reviewed and submit |

Full API docs available at `http://localhost:8000/docs` when running locally (FastAPI auto-generates Swagger UI).

---

## Roadmap

### Phase 1 — MVP Foundation (current)
- [x] Repository structure and monorepo setup
- [ ] Frontend shell with Next.js
- [ ] Backend skeleton with FastAPI
- [ ] Real-time transcription pipeline (Whisper)
- [ ] SOAP note generation (Claude)
- [ ] Nurse review dashboard (basic)

### Phase 2 — Session Architecture
- [ ] Multi-session support per nurse
- [ ] Session persistence and recovery
- [ ] Audio streaming over WebSocket
- [ ] Transcript segmentation and speaker detection

### Phase 3 — EHR Integration
- [ ] EHR adapter interface (FHIR-ready)
- [ ] One-click note submission
- [ ] Draft auto-save and version history

### Phase 4 — Production Hardening
- [ ] HIPAA compliance audit
- [ ] End-to-end encryption
- [ ] Role-based access control
- [ ] Audit trail for all AI actions
- [ ] Admin dashboard for clinic managers

---

## Screenshots

> Screenshots will be added as the MVP is built out.

| Feature | Preview |
|---------|---------|
| Nurse Dashboard | _coming soon_ |
| Live Transcription | _coming soon_ |
| SOAP Note Review | _coming soon_ |
| Session Management | _coming soon_ |

---

## Contributing

This is an early-stage startup project. Contributions are welcome once the core MVP is stable.

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes with clear, plain messages
4. Push to your fork and open a pull request
5. Keep PRs small and focused on one thing

Please do not open PRs that mix features, refactors, and bug fixes in the same diff.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

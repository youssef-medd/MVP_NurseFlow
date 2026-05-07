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

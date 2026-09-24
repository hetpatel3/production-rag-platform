# Production RAG Platform

A production-style Retrieval-Augmented Generation backend — not a 
tutorial chat-with-PDF clone. Built incrementally with hybrid 
retrieval, evaluation rigor, and real production concerns 
(auth, caching, observability, deployment) planned across phases.

## Stack
FastAPI · Qdrant · sentence-transformers (all-MiniLM-L6-v2) · Groq API

## Architecture
- `app/core` — settings, shared Qdrant client
- `app/ingestion` — chunking, embedding, storing documents
- `app/retrieval` — vector search
- `app/generation` — prompt construction, LLM calls
- `app/api` — FastAPI routes and request/response schemas

## Run locally
1. `python -m venv .venv && .venv\Scripts\Activate.ps1`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your Groq API key
4. `docker compose up -d`
5. `uvicorn main:app --reload`
6. Open `http://127.0.0.1:8000/docs`
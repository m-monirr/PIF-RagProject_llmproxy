# 🏗️ PIF RAG Chat - System Architecture

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system for querying PIF annual reports.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          Frontend (Streamlit)                    │
│                            app.py                                │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ 1. user question + chat history
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (RAG Engine)                        │
│                 api_code/rag_query.py                           │
└─┬──────────────────────┬─────────────────────┬─────────────────┘
  │                      │                      │
  │ 2. user question     │ 4. similarity       │ 6. question +
  │                      │    search            │    context +
  │                      │                      │    history
  ▼                      ▼                      ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
│  Embeddings  │  │ Vector Store │  │    LLM Proxy         │
│   Generator  │  │   (Qdrant)   │  │ (Groq/Ollama Cloud)  │
│              │  │              │  │                      │
│   Ollama     │  │  Port 6333   │  │  Port 4000          │
│ qwen3-embed  │  │              │  │ llama-3.1-8b        │
└──────────────┘  └──────────────┘  └──────────────────────┘
  │                      │                      │
  │ 3. embedding         │ 5. similar docs      │ 7. bot answer
  │                      │                      │
  └──────────────────────┴──────────────────────┘
```

## Component Details

### 1. Frontend (`app.py`)
- **Technology**: Streamlit
- **Purpose**: User interface for chat
- **Features**:
  - Real-time chat interface
  - Message history
  - Follow-up suggestions
  - Bilingual support (EN/AR)

### 2. Backend (`api_code/rag_query.py`)
- **Technology**: Python
- **Purpose**: RAG orchestration
- **Functions**:
  - `search_multiple_collections()` - Multi-year search
  - `generate_answer_from_context()` - LLM integration
  - `get_rag_answer()` - Main entry point

### 3. Embeddings Generator (`api_code/embedding.py`)
- **Technology**: Ollama (`qwen3-embedding`)
- **Dimension**: 4096
- **Purpose**: Convert text to vectors
- **API**: `http://localhost:11434`

### 4. Vector Store (`api_code/qdrant_utils.py`)
- **Technology**: Qdrant (Docker)
- **Purpose**: Store and search document embeddings
- **API**: `http://localhost:6333`
- **Collections**:
  - `PIF Annual Report 2021_collection` (EN)
  - `PIF Annual Report 2022_collection` (EN)
  - `PIF-2023-Annual-Report-EN_collection`
  - `PIF Annual Report 2021-ar_collection` (AR)
  - `PIF Annual Report 2022-ar_collection` (AR)
  - `PIF-2023-Annual-Report-AR_collection`

### 5. LLM Proxy (`api_code/llm_proxy.py`)
- **Technology**: LiteLLM + Groq/Ollama Cloud
- **Purpose**: Generate natural language answers
- **API**: `http://localhost:4000`
- **Models**:
  - **Primary**: `groq/llama-3.1-8b-instant` (FAST!)
  - **Fallback 1**: `ollama_chat/qwen2.5:latest`
  - **Fallback 2**: `ollama_chat/llama3.2:latest`
  - **Fallback 3**: `groq/mixtral-8x7b-32768`

## Data Flow

```
1. User enters question → app.py
2. Question sent to rag_query.py
3. Question embedded → embedding.py → Ollama
4. Similarity search → qdrant_utils.py → Qdrant
5. Top 5 relevant chunks retrieved
6. Question + context + history → llm_proxy.py
7. LLM generates answer → Groq/Ollama Cloud
8. Answer returned → app.py → User sees response
```

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend | Streamlit | Latest |
| Backend | Python | 3.8+ |
| Embeddings | Ollama (qwen3) | 4096-dim |
| Vector DB | Qdrant | Latest |
| LLM Proxy | LiteLLM | Latest |
| LLM Primary | Groq (llama-3.1) | 8B params |
| LLM Fallback | Ollama Cloud | 2.5B-3B params |

## Configuration Files

- **`.env`**: Environment variables (API keys, URLs)
- **`llm_proxy_config.yaml`**: LLM routing and fallback
- **`api_code/config.py`**: Model and dimension settings

## Monitoring & Debugging

- **Health Checks**: `check_services.py`
- **Debug Mode**: Enable in Streamlit sidebar
- **Logs**: Console output with logging module

## Deployment

See `RUN_GUIDE.md` for detailed startup instructions.

---

**Last Updated**: 2024-01-20
**Version**: 2.0

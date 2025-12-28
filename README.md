# NovusAI

**NovusAI** is an agent-orchestrated biomedical intelligence platform designed to perform structured analysis across **clinical evidence, scientific literature, market data, patents, web intelligence, and internal knowledge**.  
The system emphasizes **deterministic orchestration, conversation memory, and reproducible synthesis**, with optional large-model reasoning powered by **Groq-hosted LLMs**.

This repository represents a **fully working prototype** focused on architectural clarity, correctness, and explainability rather than production hardening.

---

## Core Capabilities

- **Multi-agent orchestration** with clean separation of concerns
- **Conversation-aware analysis**
  - Persistent state
  - Replayable conversations
  - Deterministic follow-ups
- **Literature-first biomedical reasoning**
- **PDF ingestion and analysis**
- **Structured synthesis (not free-form chat)**
- **Visualization-ready outputs**
- **LLM augmentation only where it adds value**

---

## Agents Overview

NovusAI uses a **modular agent architecture**, where each agent operates independently and reports structured outputs to the synthesis layer.

### Implemented Agents

- **Clinical Agent**
  - Mechanism of action
  - Clinical trial signals
  - Safety and efficacy summaries

- **Literature Agent**
  - Scientific paper analysis
  - PDF ingestion and parsing
  - Evidence-backed reasoning (abstracts, findings, conclusions)

- **Market Agent**
  - Drug-only, condition-only, and drug–condition market views
  - Deterministic data sourcing via curated mock datasets

- **Patent Agent**
  - Drug–condition intellectual property signals
  - Early-stage innovation indicators

- **Web Intelligence Agent**
  - Public discourse and external signals
  - Lightweight aggregation logic

- **Internal Knowledge Agent**
  - Private datasets
  - Organization-specific insights

---

## Architecture Overview

```mermaid
graph TD
    %% Node Definitions
    User([Client / Frontend])
    Orch[FastAPI Orchestrator]
    Router{Agent Router}
    Synth[Synthesis Engine]
    
    subgraph ContextLayer [Pre-Processing & Context]
        Entity[Entity Extraction]
        Intent[Intent Classification]
        State[Conversation State Manager]
        DB[(Persistent DB)]
    end

    subgraph Agents [Specialist Intelligence Layer]
        Clin[Clinical Agent]
        Lit[Literature Agent]
        Mark[Market Agent]
        Pat[Patent Agent]
        Web[Web Agent]
        Int[Internal Knowledge]
    end

    %% Flow Connections
    User -->|Natural Language Query| Orch
    Orch --> Entity
    Entity --> Intent
    Intent --> State
    State <--> DB
    State --> Router

    Router --> Clin
    Router --> Lit
    Router --> Mark
    Router --> Pat
    Router --> Web
    Router --> Int

    Clin & Lit & Mark & Pat & Web & Int --> Synth
    Synth -->|Structured JSON Response| User

    %% Styling / Beauty
    classDef userNode fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b;
    classDef orchNode fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#e65100;
    classDef contextNode fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
    classDef agentNode fill:#e8f5e9,stroke:#1b5e20,stroke-width:1px;
    classDef routerNode fill:#ffebee,stroke:#b71c1c,stroke-width:2px;
    classDef synthNode fill:#e0f2f1,stroke:#004d40,stroke-width:2px;

    class User userNode;
    class Orch orchNode;
    class Entity,Intent,State,DB contextNode;
    class Clin,Lit,Mark,Pat,Web,Int agentNode;
    class Router routerNode;
    class Synth synthNode;

    %% Subgraph Styling
    style ContextLayer fill:#fafafa,stroke:#9e9e9e,stroke-dasharray: 5 5
    style Agents fill:#fafafa,stroke:#9e9e9e,stroke-dasharray: 5 5
```

## Project Setup
```text
NovusAI/
├── backend/
│   └── app/
│       ├── agents/             # Domain-specific AI logic (Clinical, Patent, Market, etc.)
│       ├── api/                # FastAPI routes & endpoint definitions
│       ├── auth/               # JWT authentication & user permission logic
│       ├── db/                 # Database connection & session management
│       ├── llm/                # LLM provider integrations (Groq, etc.)
│       ├── models/             # SQLAlchemy/Pydantic data models
│       ├── mockdata/           # JSON datasets for testing (Patent & Market mocks)
│       ├── pre_synthesis/      # Query interpretation & synonym expansion
│       └── services/           # External API clients (PubMed, iCite, Patent Service)
├── frontend/
│   ├── src/
│   │   ├── api/                # Axios/Fetch clients for backend communication
│   │   ├── auth/               # AuthContext & Protected Route logic
│   │   ├── components/         # Reusable UI (Visualization, Panels, Navbar)
│   │   ├── pages/              # Main views (Chat, Scan, Admin, Profile)
│   │   └── assets/             # Static images and icons
│   ├── tailwind.config.js      # Styling configuration
│   └── vite.config.ts          # Build tool configuration
└── .gitignore                  # Environment and dependency exclusions
```

---

## Conversation State & Memory

One of the core strengths of NovusAI is **explicit conversation state management**.

### Features

- Each interaction is stored with:
  - Extracted entities
  - Intent
  - Agent outputs
  - Final synthesis
- Conversations can be:
  - Replayed cleanly
  - Continued deterministically
  - Debugged agent-by-agent
- State is persisted in a database to avoid hallucinated continuity

This enables:
- Follow-up questions without re-extraction
- Reliable comparisons
- Clean audit trails for analysis

---

## LLM Strategy (Groq)

### Important Design Decision

- **Local Ollama LLM has been removed**
- **Groq-hosted models are used for heavier reasoning**

### Why Groq?

- Significantly lower latency
- Better handling of long biomedical contexts
- More reliable for synthesis and literature reasoning

LLMs are used **selectively**, primarily for:
- Complex synthesis
- Literature interpretation
- Natural language structuring
- Entity and Intent Extraction

Rule-based logic and deterministic pipelines are preferred wherever possible.

---

## PDF & Literature Handling

- PDFs are ingested directly by conversation history and synthesis agent
- Output include user query and synthesis agent answer along with chart etc.

---

## Visualizations

- Agent outputs are structured to support:
  - Charts
  - Tables
  - Comparative views
- Visualization logic is kept separate from reasoning
- Enables clean frontend or notebook rendering

---

## Tech Stack

### Backend
- Python 3.10+
- FastAPI
- Pydantic
- httpx
- Conda-managed environment
- Groq API (LLM)
- Hugging Face models (entity extraction / intent classification)

### Frontend
- React
- MantineUI

---

## Environment Setup (Conda)

### Create Environment

```bash
conda create -n novusai python=3.10
conda activate novusai
```

### Generate/Install Dependencies

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Frontend

```bash
npm install
```
## How to Run ?

### Backend

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
npm run dev
```

## Screenshots 

## Author
Devashish Mishra
B.Tech | AI & Systems Engineering
Project: NovusAI

### Keys are hardcoded in each agents code replace them with your keys before running
## Keys Required

- Groq Key
- EPO OPS Key

### Thank You 

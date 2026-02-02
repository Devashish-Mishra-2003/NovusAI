# NovusAI – Advanced Agentic RAG for Drug Repurposing

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232d.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Mantine](https://img.shields.io/badge/Mantine-339AF0?style=for-the-badge&logo=Mantine&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-orange?style=for-the-badge)

NovusAI is an **advanced Agentic RAG (Retrieval-Augmented Generation)** system for drug repurposing and biomedical intelligence.  
It orchestrates multiple specialized agents to retrieve evidence from heterogeneous biomedical sources, synthesize insights using a large language model, and generate structured answers with visual analytics.

Unlike traditional RAG, NovusAI uses an agentic orchestration layer where each retriever is an autonomous agent operating on domain-specific sources. Evidence is merged and ranked before synthesis, enabling explainable, multi-hop biomedical reasoning.

The system supports private document ingestion, persistent sessions, and automated report generation.

## Live Deployment

- **Frontend (Netlify):** [Live Link](https://novusai.netlify.app/)
- **Backend (Render):** https://novusai-backend.onrender.com

## Use Case: Accelerating Drug Repurposing
Traditional biomedical research is siloed—patent data, clinical trials, and academic literature rarely talk to each other. **NovusAI** solves this by acting as an autonomous research assistant that:
* **Identifies New Pathways:** Cross-references existing FDA-approved drugs with new disease targets found in recent PubMed literature.
* **Risk Mitigation:** Scans clinical trial failures and patent legalities to assess the feasibility of repurposing.
* **Rapid Synthesis:** Reduces weeks of manual literature review into seconds of structured, cited intelligence.

## Key Features
* **Multi-Agent Orchestration:** 6+ specialized agents (Patent, Clinical, Literature, Web, Market, Internal) working in parallel.
* **Biomedical Entity Intelligence:** Integrated with **EBI OLS4 API** for automated drug/disease entity extraction and synonym expansion.
* **Private Knowledge Vault:** Secure RAG for internal proprietary documents (.pdf, .txt) using **Supabase Vector Storage**.
* **Visual Analytics Engine:** Converts complex evidence data into interactive charts (ReCharts) for market trends and patient outcomes.
* **Explainable AI:** Every insight includes inline citations and source-linking to the original research or patent filing.
* **Contextual Memory:** Persistent session states allowing for iterative, multi-turn biomedical discovery.

## Screenshot
## 📸 Product Interface

<table border="0">
  <tr>
    <td>
      <p align="center"><b>Main Intelligence Dashboard</b></p>
      <img src="https://github.com/user-attachments/assets/97ea795e-4bc0-40cd-ab28-427ae714122f" width="100%" />
    </td>
    <td>
      <p align="center"><b>JWT Based Login/Signup</b></p>
      <img src="https://github.com/user-attachments/assets/13216115-553d-4995-8de4-337f330b36de" width="100%" />
    </td>
  </tr>
  <tr>
    <td>
      <p align="center"><b>Employee Approval Page</b></p>
      <img src="https://github.com/user-attachments/assets/dc6f62c9-10b9-4d9e-8c87-b875d202c503" width="100%" />
    </td>
    <td>
      <p align="center"><b>Main Research Agent</b></p>
      <img src="https://github.com/user-attachments/assets/15e024f3-b012-4ee6-8d50-2a16521a5e06" width="100%" />
    </td>
  </tr>
</table>

<details>
<summary>📂 <b>View Additional Modules (Knowledge Vault & PDF Reports)</b></summary>

### Private Knowledge Vault
The secure admin interface for document ingestion and vectorization.
<img src="https://github.com/user-attachments/assets/b4653e44-e6e9-40b1-9b62-f075ae7ef44f" width="100%" />

### Automated Synthesis Report
Generated high-fidelity biomedical summary.
<img src="https://github.com/user-attachments/assets/1829f27d-689d-482c-be62-a43d241a5f7c" width="100%" />

</details>

## High-Level Flow (Agentic RAG)

```mermaid
flowchart TB
    U[User Query]
    PS[Pre Synthesis]
    ORCH[Orchestration Layer]

    PAT[Patent Agent - EPO OPS]
    CLIN[Clinical Agent - ClinicalTrials]
    LIT[Literature Agent - PubMed]
    WEB[Web Intelligence - DuckDuckGo]
    MKT[Market Agent]
    INT[Internal Knowledge - Supabase]

    EVID[Evidence Builder]
    SYN[Synthesis Agent - Groq Llama 3.1]
    VIS[Visualization Agent]
    PDF[PDF Agent]
    DB[(Session Database)]

    U --> PS --> ORCH

    ORCH --> PAT
    ORCH --> CLIN
    ORCH --> LIT
    ORCH --> WEB
    ORCH --> MKT
    ORCH --> INT

    PAT --> EVID
    CLIN --> EVID
    LIT --> EVID
    WEB --> EVID
    MKT --> EVID
    INT --> EVID

    EVID --> SYN
    SYN --> VIS
    VIS --> PDF
    SYN --> DB
```

## Agentic RAG Pipeline
## 1. Pre-Synthesis Layer
The entry point focuses on linguistic precision and query expansion.
* **Entity Extraction:** Automatically isolates **Disease** and **Drug** entities from natural language queries.
* **Synonym Expansion:** Connects to the [EBI OLS4 API](https://www.ebi.ac.uk/ols4/api) to build comprehensive synonym sets, ensuring the search covers all scientific and trade names.

## 2. Orchestration & Retrieval
A parallelized agentic layer that queries diverse data silos simultaneously.

| Agent | Source | Data Domain |
| :--- | :--- | :--- |
| **Patent Agent** | **EPO OPS** | Intellectual property, chemical filings, and legal status. |
| **Clinical Agent** | **ClinicalTrials.gov** | Study phases, recruitment status, and primary endpoints. |
| **Literature Agent** | **PubMed** | Academic journals and peer-reviewed clinical research. |
| **Web Intel Agent** | **DuckDuckGo** | Real-time news, press releases, and market alerts. |
| **Market Agent** | **Mock Data** | Commercial trends, pricing, and competitive landscape. |
| **Internal Agent** | **Supabase** | Proprietary documents and historical knowledge. |

## 3. Data Processing & Synthesis
Transforming raw, heterogeneous data into structured intelligence.

### Evidence Builder
* **Normalization:** Standardizes units, dates, and nomenclature across all 6 agents.
* **Merging:** Deduplicates information and ranks evidence based on source credibility.

### LLM Synthesis
* **Engine:** Groq API
* **Model:** `llama-3.3-70b-versatile`
* **Output:** Generates high-fidelity summaries with inline citations.

## 4. Analytics & Visualization
The system prepares JSON-ready objects for front-end rendering:
* **Market Trends:** Historical and projected growth curves.
* **Patient Outcomes:** Comparative bar charts (Treated vs. Untreated).
* **Clinical Roadmap:** Pie charts or timelines showing Study Phases (I, II, III, IV).

## 5. Persistence & Continuity
* **Storage:** Saves synthesized answers to a permanent database.
* **Session State:** Enables "rebuild" functionality where the model remembers previous context for iterative discovery.

## Private Knowledge Vault (Admin Only)
- File types: .pdf, .txt
- Storage: Supabase (company_docs bucket)
- Used by Internal Knowledge Agent

## Authentication
- JWT-based
Roles:
- admin → upload documents
- employee → query only

---

## Technical Challenges & Solutions

Building a multi-agent system for biomedical data presented several "real-world" hurdles. Below is how I engineered past them:

### 1. Model Reliability & Constraint Following
* **Challenge:** Initial testing with local models (Ollama/Phi) resulted in poor instruction following and hallucinated citations.
* **Solution:** Migrated to **Groq (Llama-3.3-70B)** and implemented rigorous **Prompt Engineering** with few-shot examples to ensure the model strictly adheres to biomedical formatting and citation rules.

### 2. Information Noise vs. Evidence Quality
* **Challenge:** Agents initially returned a high volume of low-value data, cluttering the synthesis layer.
* **Solution:** Implemented a **Domain-Specific Ranking System**.
    * **Patents:** Ranked by expiry date and legal status.
    * **Literature:** Ranked by citation count and impact factor.
    * **Result:** Only the top 5 most authoritative pieces of evidence are passed to the LLM.

### 3. The "Sparse Search" Problem (Nomenclature)
* **Challenge:** Queries for a specific drug often failed because different sources used different names (trade names vs. chemical names), leading to near-zero results.
* **Solution:** Integrated **Synonym Expansion** via the EBI OLS4 API. The system now automatically expands a single user query into a comprehensive set of scientific and commercial synonyms before the agents begin retrieval.

### 4. Resolving Contradictory Agent Intelligence
* **Challenge:** Agents occasionally provided conflicting information (e.g., a web alert claiming a drug failure vs. a patent filing showing active development).
* **Solution:** Developed a **Source-Credibility Scoring Matrix**. I assigned weighted priority to data sources: 
    * `Patent Data (High)` > `Clinical Trials` > `Literature` > `Web Intel (Low)`.
    * The LLM is prompted to prioritize "Source Truth" based on these weights when synthesizing the final report.

## Tech Stack
### Backend
- FastAPI
- SQLAlchemy
- JWT
- Supabase Storage
- Groq API

### Frontend
- React + Vite
- Mantine UI
- Axios
- ReCharts

### Deployment
- Backend → Render
- Frontend → Netlify

## Local Setup
### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables (Backend)
```bash
SUPABASE_URL=xxxxxxxxxx
SUPABASE_SERVICE_KEY=xxxxxxxxxx
SUPABASE_ANON_KEY=xxxxxxxxxx
JWT_SECRET_KEY=xxxxxxxxxx
JWT_ALGORITHM=xxxxxxxxxx
ENV=xxxxxxxxxx
PUBLIC_API_URL=xxxxxxxxxx
GROQ_API_KEY=xxxxxxxxxx
GROQ_BASE_URL=xxxxxxxxxx
MODEL_NAME=xxxxxxxxxx
CONSUMER_KEY=xxxxxxxxxx
CONSUMER_SECRET=xxxxxxxxxx
```

## Environment Variables (Frontend)
```bash
VITE_API_BASE_URL=https://<backend-url>
```

## Repository Structure
```bash
NovusAI/
  backend/
  frontend/
```

## Author
Devashish Mishra
B.Tech | AI/ML | Full-Stack | Cloud

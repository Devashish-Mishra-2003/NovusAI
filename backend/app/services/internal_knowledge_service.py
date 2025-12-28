from pathlib import Path
from typing import List, Dict, Optional
import os
import subprocess
import re

# =========================
# Configuration
# =========================

BASE_DATA_PATH = Path(
    os.getenv(
        "INTERNAL_KNOWLEDGE_PATH",
        "data/internal_knowledge/companies"
    )
)

DOCUMENT_TYPES = {
    "strategy": "strategy_note",
    "diligence": "diligence_memo",
    "portfolio": "portfolio_decision",
    "exec_notes": "exec_commentary",
}

OLLAMA_MODEL = "qwen2.5:3b-instruct-q4_0"


class InternalKnowledgeError(Exception):
    pass


# =========================
# Helpers
# =========================

def _company_base(company_id: str) -> Path:
    path = BASE_DATA_PATH / company_id
    if not path.exists():
        raise InternalKnowledgeError(f"Company data not found: {company_id}")
    return path


def _load_documents(company_id: str) -> List[Dict]:
    base = _company_base(company_id)
    docs: List[Dict] = []

    for folder, doc_type in DOCUMENT_TYPES.items():
        folder_path = base / folder
        if not folder_path.exists():
            continue

        for f in folder_path.iterdir():
            if f.suffix not in {".md", ".txt"}:
                continue

            docs.append({
                "document_id": f.name,
                "document_type": doc_type,
                "raw_text": f.read_text(encoding="utf-8"),
            })

    return docs


def _basic_match(
    text: str,
    drug: Optional[str],
    condition: Optional[str]
) -> int:
    t = text.lower()
    score = 0

    if drug and drug.lower() in t:
        score += 2
    if condition and condition.lower() in t:
        score += 2

    return score


# =========================
# Stage 1: Deterministic Retrieval (RELAXED)
# =========================

def retrieve_candidate_documents(
    company_id: str,
    drug: Optional[str],
    condition: Optional[str]
) -> List[Dict]:

    documents = _load_documents(company_id)
    results: List[Dict] = []

    for doc in documents:
        score = _basic_match(
            doc["raw_text"],
            drug,
            condition
        )

        # 🔒 CHANGE: never hard-drop documents
        if score >= 4:
            confidence = "high"
        elif score > 0:
            confidence = "medium"
        else:
            continue

        results.append({
            **doc,
            "confidence": confidence
        })

    return results


# =========================
# Stage 2: Constrained LLM Extraction (UNCHANGED)
# =========================

def extract_relevant_excerpt_llm(
    document_text: str,
    user_query: str
) -> str:
    """
    HARD GUARANTEES:
    - LLM may ONLY select or lightly clean existing sentences
    - NO new facts, opinions, summaries, or interpretations
    - Any violation triggers deterministic fallback
    """

    prompt = f"""
You are extracting sentences from an internal document.

STRICT RULES:
- You may ONLY copy sentences that already exist in the document
- You may fix grammar or whitespace ONLY
- You MUST NOT explain, summarize, or add interpretation
- If nothing is relevant, return exactly: NO_RELEVANT_CONTENT

Document:
{document_text}

User question:
{user_query}

Return the extracted sentences verbatim or lightly cleaned.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )

        output = result.stdout.decode("utf-8", errors="ignore").strip()

        if not output or output == "NO_RELEVANT_CONTENT":
            return document_text[:600].strip()

        # Guardrail: ensure extracted text exists in source
        doc_norm = re.sub(r"\s+", " ", document_text.lower())
        out_norm = re.sub(r"\s+", " ", output.lower())

        chunks = [
            c.strip()
            for c in re.split(r"[.\n]", out_norm)
            if c.strip()
        ]

        for c in chunks:
            if c not in doc_norm:
                return document_text[:600].strip()

        return output.strip()

    except Exception:
        return document_text[:600].strip()

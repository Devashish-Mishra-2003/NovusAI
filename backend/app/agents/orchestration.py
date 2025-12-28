# app/agents/orchestration.py

from fastapi import APIRouter, Response
from pydantic import BaseModel, Field
from typing import List, Dict
import httpx
import logging

logger = logging.getLogger("orchestration")
router = APIRouter()

BASE_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# AGENT ENDPOINTS (LOCKED)
# --------------------------------------------------
AGENT_ENDPOINTS = {
    "clinical": "/api/clinical",
    "literature": "/api/literature",
    "patents": "/api/patents",
    "market": "/api/market",
    "web": "/api/web_intelligence",
    "internal": "/api/internal-knowledge",
    # "visualization": "/api/visualize",  # STILL DISABLED
}

# --------------------------------------------------
# INTENT → AGENT GROUP MAP (LOCKED)
# --------------------------------------------------
INTENT_AGENT_MAP = {
    "CLINICAL": ["clinical", "literature"],
    "COMMERCIAL": ["market", "patents", "web"],
    "INTERNAL": ["internal"],
    "FULL_OPPORTUNITY": [
        "clinical",
        "literature",
        "market",
        "patents",
        "web",
        "internal",
    ],
}

# --------------------------------------------------
# INPUT SCHEMA ONLY (NO OUTPUT MODEL)
# --------------------------------------------------
class OrchestrationRequest(BaseModel):
    drug: str = Field(default="")
    conditions: List[str] = Field(default_factory=list)
    intent: str


# --------------------------------------------------
# EVIDENCE BUNDLE BUILDER
# --------------------------------------------------
def build_evidence_bundle(agent_outputs: Dict[str, str]) -> str:
    parts: List[str] = []
    parts.append("=== EVIDENCE BUNDLE START ===\n\n")

    for agent, text in agent_outputs.items():
        parts.append(f"[AGENT: {agent.upper()}]\n")
        parts.append(text.strip())
        parts.append("\n\n")

    parts.append("=== EVIDENCE BUNDLE END ===")
    return "".join(parts)


# --------------------------------------------------
# ORCHESTRATION ENDPOINT — PLAIN TEXT ONLY
# --------------------------------------------------
@router.post("/orchestrate")
async def orchestrate(req: OrchestrationRequest):
    intent = req.intent.upper()

    if intent not in INTENT_AGENT_MAP:
        logger.error("Unsupported intent: %s", intent)
        return Response(
            content=f"ERROR: Unsupported intent '{intent}'",
            media_type="text/plain",
            status_code=400,
        )

    agents_to_call = INTENT_AGENT_MAP[intent]
    logger.info("Orchestration started | intent=%s | agents=%s", intent, agents_to_call)

    payload = {
        "drug": req.drug,
        "conditions": req.conditions,
    }

    agent_outputs: Dict[str, str] = {}

    async with httpx.AsyncClient(timeout=90) as client:
        for agent in agents_to_call:
            logger.info("Calling agent: %s", agent)
            resp = await client.post(
                f"{BASE_URL}{AGENT_ENDPOINTS[agent]}",
                json=payload,
            )

            if resp.status_code != 200:
                logger.error("Agent %s failed | status=%s", agent, resp.status_code)
                agent_outputs[agent] = "ERROR: Agent call failed."
            else:
                # 🔒 RAW PLAIN TEXT — NO PARSING
                agent_outputs[agent] = resp.text

    evidence_text = build_evidence_bundle(agent_outputs)

    logger.info("Orchestration completed successfully")

    return Response(
        content=evidence_text,
        media_type="text/plain",
    )

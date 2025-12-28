# app/pre_synthesis/groq_interpreter.py

import re
import logging
from typing import Dict, List

from openai import OpenAI
from app.pre_synthesis.condition_synonyms import expand_condition

logger = logging.getLogger("groq-interpreter")

# ======================================================
# CONFIG — GROQ
# ======================================================

GROQ_API_KEY = "supersecretkey"  # ← Your key
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.1-8b-instant"  # Fast + cheap for extraction  # Best balance of quality, speed, and reasoning

client = OpenAI(
    base_url=GROQ_BASE_URL,
    api_key=GROQ_API_KEY,
)

# ======================================================
# SYSTEM PROMPT (LOCKED — PERFECT FOR BIOMEDICAL INTENT EXTRACTION)
# ======================================================

SYSTEM_PROMPT = """
You are a biomedical query interpreter.

Your task is to extract:
1) the primary drug (if any),
2) the primary disease or condition (if any),
3) the user intent.

You must follow ALL rules strictly.

OUTPUT FORMAT (EXACTLY 3 LINES):
DRUG: <comma-separated drug names or NONE>
CONDITION: <condition name or NONE>
INTENT: <ONE OF THE VALUES BELOW>

ALLOWED INTENT VALUES:
- CLINICAL
- COMMERCIAL
- INTERNAL
- FULL_OPPORTUNITY
- GENERAL

WHAT EACH INCLUDES : 
- CLINICAL: Clinical and Literature
- COMMERCIAL : Maket, Patents, Web
- INTERNAL : Company Data, Internal Research
- FULL_OPPORTUNITY : All Data Sources
- GENERAL : General chitchat or non-specific queries

RULES:
- Output ONLY the 3 lines above.
- Use NONE if drug or condition is not explicitly mentioned or strongly implied.
- Do NOT explain.
- Do NOT add extra text.
- Do NOT add examples.
- Do NOT add confidence scores.
- End output immediately after the INTENT line.
""".strip()

# ======================================================
# NORMALIZATION
# ======================================================

_BRACKET_RE = re.compile(r"\s*\(.*?\)\s*")


def _normalize_text(value: str) -> str:
    value = _BRACKET_RE.sub("", value)
    value = re.sub(r"\s+", " ", value).strip().lower()
    return value


# ======================================================
# PARSER
# ======================================================

def _parse_llm_output(text: str) -> Dict[str, object]:
    lines = []

    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("<s>"):
            line = line.replace("<s>", "").strip()
        if line.startswith(("DRUG:", "CONDITION:", "INTENT:")):
            lines.append(line)

    if len(lines) != 3:
        raise ValueError(f"Invalid LLM output: expected 3 lines, got {lines}")

    def extract(prefix: str, line: str) -> str:
        if not line.startswith(prefix):
            raise ValueError(f"Expected {prefix}, got {line}")
        return line[len(prefix):].strip()

    # ---- DRUGS (LIST) ----
    raw_drug = extract("DRUG:", lines[0])
    if raw_drug.upper() == "NONE":
        drugs: List[str] = []
    else:
        drugs = [
            _normalize_text(d.strip())
            for d in raw_drug.split(",")
            if d.strip()
        ]

    # ---- CONDITION ----
    raw_condition = extract("CONDITION:", lines[1])
    condition = None if raw_condition.upper() == "NONE" else _normalize_text(raw_condition)

    # ---- INTENT ----
    intent = extract("INTENT:", lines[2]).strip().upper()

    return {
        "drug": drugs,
        "condition": condition,
        "intent": intent,
    }


# ======================================================
# PUBLIC API
# ======================================================

def interpret_query(query: str) -> Dict[str, object]:
    """
    Returns:
    {
        "drug": List[str],
        "conditions": List[str],  # expanded via synonyms
        "intent": str
    }
    """
    if not query or not query.strip():
        return {
            "drug": [],
            "conditions": [],
            "intent": "GENERAL",
        }

    logger.info("🔎 Interpreting query via Groq (Llama 3.3 70B)")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=60,
    )

    raw_text = response.choices[0].message.content.strip()
    logger.debug(f"Groq interpreter raw output:\n{raw_text}")

    parsed = _parse_llm_output(raw_text)

    # ---- CONDITION SYNONYM EXPANSION ----
    condition = parsed.get("condition")
    if condition and len(condition.split()) > 8:  # safety
        condition = None

    conditions = expand_condition(condition) if condition else []

    return {
        "drug": parsed.get("drug", []),
        "conditions": conditions,
        "intent": parsed["intent"],
    }
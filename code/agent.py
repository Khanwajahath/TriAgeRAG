import os
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from google import genai

from retriever import retrieve

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM = """You are a support triage agent. You must:
- Classify the ticket using ONLY the provided context.
- NEVER invent policies or facts not in the context.
- Escalate if: billing dispute, fraud, account lock, legal threat,
  sensitive personal data, or if the corpus has no relevant answer.
- Reply only if you can give a grounded, accurate answer.

Output ONLY valid JSON with these keys:
  status, product_area, response, justification, request_type

status: 'replied' or 'escalated'
request_type: 'product_issue', 'feature_request', 'bug', 'invalid'
"""

 
MODEL_SEQUENCE = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

REQUIRED_KEYS = {
    "status",
    "product_area",
    "response",
    "justification",
    "request_type",
}

ALLOWED_STATUS = {"replied", "escalated"}
ALLOWED_REQUEST_TYPES = {"product_issue", "feature_request", "bug", "invalid"}

 
LOG_DIR = Path.home() / "hackerrank_orchestrate"
LOG_FILE = LOG_DIR / "log.txt"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_chat(role: str, content: str):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] {role}\n")
        f.write(content.strip() + "\n")
        f.write("=" * 80 + "\n")


def _build_prompt(company: str, subject: str, issue: str, context: str) -> str:
    return f"""TICKET
Company: {company}
Subject: {subject}
Issue: {issue}

SUPPORT CORPUS CONTEXT:
{context}

Respond with JSON only."""


def _extract_json(raw: str) -> Dict:
    raw = raw.replace("```json", "").replace("```", "").strip()

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON found")

    return json.loads(raw[start:end + 1])


def _validate(data: Dict) -> bool:
    if not isinstance(data, dict):
        return False

    if not REQUIRED_KEYS.issubset(data.keys()):
        return False

    if data["status"] not in ALLOWED_STATUS:
        return False

    if data["request_type"] not in ALLOWED_REQUEST_TYPES:
        return False

    return True


def _call_model(model_name: str, prompt: str) -> Optional[Dict]:
    try:
        print(f"Trying model: {model_name}")

        response = client.models.generate_content(
            model=model_name,
            contents=[{
                "role": "user",
                "parts": [{"text": f"{SYSTEM}\n\n{prompt}"}]
            }]
        )

        raw = getattr(response, "text", "")

        data = _extract_json(raw)

        if _validate(data):
            return data

        return None

    except Exception as e:
        print(f"{model_name} failed: {e}")
        return None


def triage(issue: str, subject: str, company: str) -> dict:
    print("==== TRIAGE INPUT ====")
    print(f"Company : {company}")
    print(f"Subject : {subject}")
    print(f"Issue   : {issue}")
    print("=======================\n")

    context_chunks = retrieve(issue, company=company)
    context = "\n\n---\n\n".join(context_chunks)

 

    prompt = _build_prompt(company, subject, issue, context)

     
    log_chat("USER", f"""
Company: {company}
Subject: {subject}
Issue: {issue}

Context:
{context}
""")

    # ✅ Try models in order
    for model_name in MODEL_SEQUENCE:
        result = _call_model(model_name, prompt)

        if result is not None:
            log_chat("ASSISTANT", json.dumps(result, indent=2))
            return result

    # ❗ Final fallback → Escalation
    fallback = {
        "status": "escalated",
        "product_area": "unknown",
        "response": "",
        "justification": "No valid grounded response from any model.",
        "request_type": "invalid",
    }

    log_chat("ASSISTANT", json.dumps(fallback, indent=2))
    return fallback
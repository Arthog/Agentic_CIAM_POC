import json
import re

from pydantic import BaseModel, Field

from security_engine import evaluate_abac_policy

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


# Pydantic is intentionally kept here for future schema validation and richer
# model parsing, even though a dataclass would be enough for the current PoC.
class AccessRequest(BaseModel):
    user_reference: str = Field(description="The person or user identifier requesting access")
    resource_reference: str = Field(description="The target application, data asset, or resource")
    intent: str = Field(description="A concise summary of the requested action")
    confidence: float = Field(description="Extraction confidence from 0.0 to 1.0")


def _extract_request_with_rules(user_query: str) -> AccessRequest:
    query = user_query.lower()

    user_reference = "unknown"
    if "alex" in query:
        user_reference = "alex compromised" if "untrusted" in query or "unknown" in query else "alex"
    elif "sam" in query:
        user_reference = "sam"

    resource_reference = "unknown"
    if re.search(r"\b(ledger|budget|finance|financial)\b", query):
        resource_reference = "financial_ledger"

    return AccessRequest(
        user_reference=user_reference,
        resource_reference=resource_reference,
        intent=user_query.strip(),
        confidence=0.55 if "unknown" not in {user_reference, resource_reference} else 0.25,
    )


def _extract_request_with_gemini(user_query: str) -> AccessRequest:
    if genai is None or types is None:
        raise RuntimeError("google-genai is not installed")

    client = genai.Client()
    config = types.GenerateContentConfig(
        system_instruction=(
            "You extract CIAM/ABAC access request context from natural language. "
            "Do not approve or deny access. Return only the requester, resource, "
            "intent, and confidence for a deterministic policy engine to evaluate."
        ),
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=AccessRequest,
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_query,
        config=config,
    )
    if hasattr(AccessRequest, "model_validate_json"):
        return AccessRequest.model_validate_json(response.text)

    return AccessRequest(**json.loads(response.text))


def extract_access_request(user_query: str) -> dict:
    try:
        extraction = _extract_request_with_gemini(user_query)
        source = "gemini"
        error = None
    except Exception as exc:
        extraction = _extract_request_with_rules(user_query)
        source = "rules_fallback"
        error = str(exc)

    return {
        "source": source,
        "error": error,
        "user_reference": extraction.user_reference,
        "resource_reference": extraction.resource_reference,
        "intent": extraction.intent,
        "confidence": extraction.confidence,
    }


def process_natural_language_request(user_query: str) -> dict:
    extraction = extract_access_request(user_query)
    policy_decision = evaluate_abac_policy(
        extraction["user_reference"],
        extraction["resource_reference"],
    )

    return {
        "input": user_query,
        "extraction": extraction,
        "policy_decision": policy_decision,
    }

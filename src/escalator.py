import json
from src.config import CONFIDENCE_THRESHOLD

def check_escalation(user_query: str, context_chunks: list) -> bool:
    """Checks if the query needs human escalation based on thresholds or keywords."""
    best_score = max([chunk["score"] for chunk in context_chunks]) if context_chunks else 0.0
    
    # Sensitive trigger words
    sensitive_keywords = ["refund", "sue", "lawyer", "legal", "chargeback"]
    contains_sensitive = any(word in user_query.lower() for word in sensitive_keywords)

    if best_score < CONFIDENCE_THRESHOLD or not context_chunks or contains_sensitive:
        return True
    return False

def generate_handoff_summary(user_query: str, persona: str, context_chunks: list) -> str:
    handoff_data = {
        "persona": persona,
        "detected_issue": user_query[:100] + ("..." if len(user_query) > 100 else ""),
        "retrieved_sources": [c["source"] for c in context_chunks],
        "confidence_score": max([c["score"] for c in context_chunks]) if context_chunks else 0.0,
        "recommended_action": "Review system constraints, check user logs, and connect with live agent."
    }
    return json.dumps(handoff_data, indent=2)
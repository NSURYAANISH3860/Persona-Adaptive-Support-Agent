from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, MODEL_NAME
from src.escalator import check_escalation, generate_handoff_summary

def generate_adaptive_response(user_query: str, persona: str, context_chunks: list) -> dict:
    
    # 1. Escalation Check
    if check_escalation(user_query, context_chunks):
        return {
            "escalated": True,
            "response": "I apologize, but I am unable to automatically resolve this specific request safely. I am connecting you with a live human support specialist immediately.",
            "handoff_summary": generate_handoff_summary(user_query, persona, context_chunks)
        }

    # 2. Persona Routing
    if persona == "Technical Expert":
        persona_instructions = (
            "You are a Senior Systems Engineer. Provide clear root-cause analysis, "
            "configuration specifications, and precise API pathways or code blocks. "
        )
    elif persona == "Frustrated User":
        persona_instructions = (
            "You are a deeply empathetic, reassuring Customer Care Specialist. "
            "Begin with a warm, genuine validation of their difficulty. Use straightforward, "
            "reassuring, and simple action-oriented bullet steps."
        )
    else:  
        persona_instructions = (
            "You are a concise Client Relations Director. Focus on direct business outcomes, "
            "impact summaries, and timelines for resolution. Keep responses extremely brief."
        )

    # 3. Compile Prompt
    context_text = "\n\n".join([f"Source [{c['source']}]: {c['text']}" for c in context_chunks])
    full_system_prompt = (
        f"{persona_instructions}\n\n"
        "CRITICAL RULES:\n"
        "- Base your response ONLY on the provided context.\n"
        "- Do not hallucinate or assume facts not found in the documents.\n\n"
        f"FACTUAL CONTEXT DOCUMENTS:\n{context_text}"
    )

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=full_system_prompt,
            temperature=0.2
        )
    )

    return {
        "escalated": False,
        "response": response.text,
        "handoff_summary": None
    }
import json
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, MODEL_NAME

def classify_customer_persona(user_message: str) -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)

    system_instruction = (
        "You are an advanced classification engine. Analyze the sentiment, vocabulary, "
        "and tone of the incoming message and classify it into exactly one of three personas:\n"
        "1. 'Technical Expert': Uses jargon, asks about APIs/code/configs.\n"
        "2. 'Frustrated User': Uses emotional language, exclamation marks, or mentions urgency.\n"
        "3. 'Business Executive': Focuses on business impact, ROI, timelines, and brevity.\n\n"
        "Provide your evaluation strictly in the requested JSON structure."
    )

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "persona": {
                "type": "STRING",
                "enum": ["Technical Expert", "Frustrated User", "Business Executive"]
            },
            "confidence": {"type": "NUMBER"},
            "reasoning": {"type": "STRING"}
        },
        "required": ["persona", "confidence", "reasoning"]
    }

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema,
            temperature=0.1
        )
    )
    return json.loads(response.text)
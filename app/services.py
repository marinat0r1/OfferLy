import openai
import json
from .config import settings
from .schemas import OfferResponse

# Set API key
openai.api_key = settings.OPENAI_API_KEY

# -----------------------------
# GPT call for simple questions
# -----------------------------
def call_gpt_question(prompt: str) -> str:
    """
    Ask GPT a domain-related question and return a plain text answer.
    Compatible with openai>=1.0.0
    """
    response = openai.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are an assistant for contractors."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# -----------------------------
# GPT call for structured offers
# -----------------------------
def call_gpt_offer(content: str, metadata: dict | None) -> OfferResponse:
    functions = [
        {
            "name": "generate_offer",
            "description": "Generate a structured offer for a contracting job",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_title": {"type": "string"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "unit_price": {"type": "number"},
                                "total_price": {"type": "number"}
                            },
                            "required": ["description", "quantity", "unit_price", "total_price"]
                        }
                    },
                    "total": {"type": "number"},
                    "notes": {"type": "string"}
                },
                "required": ["project_title", "items", "total"]
            }
        }
    ]

    response = openai.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are an assistant that creates professional contractor offers."},
            {"role": "user", "content": f"Create an offer for: {content}. Extra info: {metadata}"}
        ],
        functions=functions,
        function_call={"name": "generate_offer"}
    )

    try:
        # ← fixed line
        arguments = response.choices[0].message.function_call.arguments
        offer_data = json.loads(arguments)
    except (AttributeError, json.JSONDecodeError) as e:
        return OfferResponse(
            project_title="Error generating offer",
            items=[],
            total=0,
            notes=f"Failed to parse GPT output: {e}"
        )

    return OfferResponse(**offer_data)

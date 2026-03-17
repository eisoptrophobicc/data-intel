import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_insight(intent, data):

    if not data:
        return None

    preview = data[:10]  # prevent huge prompts

    prompt = f"""
You are a business intelligence analyst.

A query was executed with this structured intent:

{json.dumps(intent, indent=2)}

The query returned this data:

{json.dumps(preview, indent=2)}

Write a short insight summarizing the key takeaway.

Rules:
- Maximum 2 sentences
- Mention the most important value or trend
- Do NOT invent numbers
- Only use numbers that appear in the data
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    if not response.text:
        return None

    return response.text.strip()
import os
import openai
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

# Setup OpenAI and Notion clients
openai.api_key = os.getenv("OPENAI_API_KEY")
notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")


def extract_event_details(message: str):
    try:
        prompt = f"""
You are an assistant that extracts event details from text. 

Input: "{message}"

Return a JSON object with keys:
- "title" (what the event is)
- "datetime" (in ISO 8601 format)
- "location" (optional, can be null if not specified)

Respond only with the JSON object. No extra explanation.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response['choices'][0]['message']['content'].strip()

        # Try parsing the model's output as JSON
        import json
        parsed = json.loads(content)

        return parsed

    except Exception as e:
        return {
            "error": str(e),
            "message": message
        }

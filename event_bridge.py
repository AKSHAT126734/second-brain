import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from notion_client import Client

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")


def extract_event_details(message: str):
    try:
        prompt = f"""
You are an assistant that extracts event details from natural language text. 

Input: "{message}"

Return a JSON object with these keys:
- "title" (what the event is)
- "datetime" (in ISO 8601 format)
- "location" (optional, can be null if not specified)

Only respond with the JSON object.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)

        return parsed

    except Exception as e:
        return {
            "error": str(e),
            "message": message
        }

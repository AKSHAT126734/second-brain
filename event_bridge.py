import os
import openai
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
notion = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def extract_event_info_from_text(user_input: str) -> dict:
    prompt = f"""
You are a helpful assistant that extracts calendar event data from user input.

Extract the following fields:
- title
- date
- start_time (24h format, IST)
- end_time (if available, otherwise null)
- location (if available)
- description (if available)

User Input: "{user_input}"

Respond in JSON format:
{{
  "title": ...,
  "date": ...,
  "start_time": ...,
  "end_time": ...,
  "location": ...,
  "description": ...
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    json_text = response["choices"][0]["message"]["content"]
    return eval(json_text)  # assumes model returns clean JSON dict

def handle_notion_event(user_input: str):
    event = extract_event_info_from_text(user_input)

    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Name": {"title": [{"text": {"content": event["title"]}}]},
            "Date": {"date": {"start": f"{event['date']}T{event['start_time']}+05:30"}},
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": f"Location: {event.get('location', '')}"}}],
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": f"Description: {event.get('description', '')}"}}],
                },
            }
        ]
    )

import os
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client
import dateparser

load_dotenv()

def parse_event(input_text: str) -> dict:
    print("\n🧠 Parsing user input:", input_text)

    # Extract datetime
    dt = dateparser.parse(input_text, settings={'PREFER_DATES_FROM': 'future'})
    if not dt:
        raise ValueError("Could not parse datetime from input")

    # Very basic logic to extract title and location
    title = "Untitled Event"
    location = ""

    lower_text = input_text.lower()
    if " at " in lower_text:
        parts = input_text.split(" at ")
        if len(parts) >= 2:
            title = parts[0].strip().capitalize()
            location = "at " + parts[1].strip().capitalize()
        else:
            title = input_text.strip().capitalize()
    else:
        title = input_text.strip().capitalize()

    event = {
        "title": title,
        "datetime": dt,
        "location": location
    }

    print("🧾 Parsed event details:", event)
    return event

def send_to_notion(event: dict):
    print("\n📤 Attempting to send to Notion...")
    print("📝 Payload to Notion:", event)

    try:
        notion = Client(auth=os.getenv("NOTION_API_KEY"))
        response = notion.pages.create(
            parent={"database_id": os.getenv("NOTION_CALENDAR_DB_ID")},
            properties={
                "Name": {"title": [{"text": {"content": event['title']}}]},
                "Date": {"date": {"start": event['datetime'].isoformat()}},
                "Location": {"rich_text": [{"text": {"content": event.get('location', '')}}]},
            },
        )
        print("✅ Notion response:")
        print(response)
    except Exception as e:
        print("❌ Failed to send to Notion.")
        print("Error:", e)

def handle_notion_event(user_input: str):
    try:
        event = parse_event(user_input)
        send_to_notion(event)
    except Exception as e:
        print("❌ Error in handle_notion_event:")
        print(e)

import os
import json
import dateparser
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")

def extract_event_details(message: str):
    parsed_date = dateparser.parse(
        message,
        settings={"PREFER_DATES_FROM": "future"}
    )
    if not parsed_date:
        raise ValueError("Could not parse a date from the input.")

    # Simple parsing for title and location
    title = message.split(" at ")[0].strip().capitalize()
    location = None
    if " at " in message:
        location = message.split(" at ")[-1].strip()

    return {
        "title": title,
        "datetime": parsed_date.isoformat(),
        "location": location
    }

def add_event_to_notion(event: dict):
    new_page = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [
                    { "text": { "content": event["title"] } }
                ]
            },
            "Date": {
                "date": {
                    "start": event["datetime"]
                }
            }
        }
    }

    if event["location"]:
        new_page["properties"]["Location"] = {
            "rich_text": [
                { "text": { "content": event["location"] } }
            ]
        }

    # DEBUG: Show the payload being sent
    print("📤 Sending the following data to Notion:")
    print(json.dumps(new_page, indent=2))

    try:
        notion.pages.create(**new_page)
        print("✅ Event successfully added to Notion.")
    except Exception as e:
        print("❌ Failed to add event to Notion.")
        print("Error:", str(e))

def handle_notion_event(message: str):
    print("📩 Received message:", message)
    try:
        event = extract_event_details(message)
        print("🧠 Parsed event details:", event)
        add_event_to_notion(event)
    except Exception as e:
        print("❌ Error processing event:", str(e))

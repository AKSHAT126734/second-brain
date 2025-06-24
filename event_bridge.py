# 🛠️ Triggering redeploy: Minor comment added

from notion_client import Client
from datetime import datetime
import dateparser
import os

def extract_event_details(user_input: str):
    dt = dateparser.parse(user_input, settings={"PREFER_DATES_FROM": "future"})
    if not dt:
        return None

    return {
        "title": user_input.split(" at ")[0].strip().capitalize(),
        "datetime": dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "location": user_input.split(" at ")[-1].strip().capitalize() if " at " in user_input else "",
    }

def handle_notion_event(user_input: str):
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    database_id = os.getenv("NOTION_DATABASE_ID")
    event = extract_event_details(user_input)

    if not event:
        return {"error": "Could not parse date or event details."}

    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": event["title"]}}]},
            "Date": {"date": {"start": event["datetime"]}},
            "Location": {"rich_text": [{"text": {"content": event["location"]}}]},
        }
    )
    return {"message": "Event added to Notion calendar!"}

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
        return {
            "error": "❌ Could not parse a date from the input.",
            "message": message
        }

    # Very basic title/location extraction
    title = message.split(" at ")[0].strip().capitalize()
    location = None
    if " at " in message:
        location = message.split(" at ")[-1].strip()

    return {
        "title": title,
        "datetime": parsed_date.isoformat(),
        "location": location
    }

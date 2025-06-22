# event_bridge.py

import re
from datetime import datetime, timedelta
import dateparser

def handle_notion_event(payload):
    event_text = payload.get("event", "")

    # Extract date & time
    date = dateparser.parse(event_text, settings={"PREFER_DATES_FROM": "future"})
    date_str = date.strftime("%Y-%m-%d") if date else "Unknown"

    # Extract time (if dateparser doesn't catch it)
    time_match = re.search(r"\b(?:at|@)\s*(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)", event_text, re.IGNORECASE)
    time_str = time_match.group(1) if time_match else ""

    # Extract location
    location_match = re.search(r"(?:at|in)\s+([A-Z][\w\s,&-]+)", event_text)
    location = location_match.group(1).strip() if location_match else ""

    # Extract category
    category_match = re.search(r"category\s*:\s*(\w+)", event_text, re.IGNORECASE)
    category = category_match.group(1) if category_match else "general"

    # Extract description
    desc_match = re.search(r"description\s*:\s*(.+)", event_text, re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else ""

    # Use the first sentence or whole string as title fallback
    title = event_text.split('.')[0] if '.' in event_text else event_text

    return {
        "status": "received",
        "title": title.strip(),
        "date": date_str,
        "time": time_str.strip(),
        "location": location,
        "category": category,
        "description": description,
        "raw": event_text
    }

import dateparser
import re
from datetime import datetime

def handle_notion_event(event_text: str) -> dict:
    # Extract datetime from natural text
    dt = dateparser.parse(event_text, settings={"PREFER_DATES_FROM": "future"})
    
    if not dt:
        return {
            "status": "error",
            "message": "Could not parse date or time"
        }

    # Try to find location (basic: last capitalized word group)
    location_match = re.search(r"in ([A-Z][a-zA-Z\s]+)", event_text)
    location = location_match.group(1).strip() if location_match else "Unknown"

    # Try to extract a meaningful title
    title_match = re.search(r"(?:have|got|need|going)\s+to\s+(.*?)\s+(?:in|at|on|by|$)", event_text)
    title = title_match.group(1).strip().capitalize() if title_match else event_text[:30]

    return {
        "status": "received",
        "title": title,
        "date": dt.strftime("%Y-%m-%d"),
        "time": dt.strftime("%H:%M"),
        "location": location,
        "description": event_text,
        "category": "personal"
    }

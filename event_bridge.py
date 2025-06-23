# event_bridge.py

from typing import Optional
import dateparser
import re

def extract_event_details(text: str) -> dict:
    result = {
        "title": text.strip(),
        "date": None,
        "time": None,
        "location": None,
        "description": text.strip(),
        "category": "general"
    }

    # Extract datetime
    dt = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})
    if dt:
        result["date"] = dt.strftime("%Y-%m-%d")
        result["time"] = dt.strftime("%H:%M")

    # Extract location (very basic — after keywords like 'at', 'in', etc.)
    location_match = re.search(r'\b(?:at|in|to)\s+([A-Z][\w\s]+)', text)
    if location_match:
        result["location"] = location_match.group(1).strip()

    # Attempt to extract cleaner title
    title_match = re.search(r'(?:I have|there is|attend)\s+(.*?)\s+(?:at|in|on|by|tomorrow|today|next|this|at\s+\d)', text, re.IGNORECASE)
    if title_match:
        result["title"] = title_match.group(1).strip().capitalize()

    return result

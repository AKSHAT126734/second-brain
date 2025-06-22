# event_bridge.py

import dateparser
import re

def extract_datetime(text):
    dt = dateparser.parse(text)
    if dt:
        date = dt.date().isoformat()
        time = dt.time().strftime("%H:%M") if dt.time() else ""
        return date, time
    return "Unrecognized", ""

def extract_location(text):
    # Naive rule-based location extraction (you can replace this with spaCy for better results)
    match = re.search(r"in ([A-Za-z\s]+)", text)
    return match.group(1).strip() if match else ""

def extract_title(text):
    # Try to extract the purpose (e.g., "doctor's appointment", "wedding", "exam")
    key_phrases = ['meeting', 'appointment', 'exam', 'class', 'lecture', 'party', 'wedding', 'birthday']
    for phrase in key_phrases:
        if phrase in text.lower():
            return ' '.join([word.capitalize() for word in text.split() if phrase in word.lower()])
    return text.split("at")[-1].strip().capitalize()

def handle_notion_event(payload):
    raw_text = payload.get("event", "")
    date, time = extract_datetime(raw_text)
    location = extract_location(raw_text)
    title = extract_title(raw_text)

    return {
        "status": "received",
        "title": title,
        "date": date,
        "time": time,
        "location": location,
        "description": raw_text,
        "category": "general"
    }

import dateparser

def handle_notion_event(payload):
    text = payload if isinstance(payload, str) else payload.get("event", "")
    
    # Basic parsing
    parsed_date = dateparser.parse(text)

    # Simple rule-based extraction (you can improve this later)
    title = text.strip()
    date = parsed_date.date().isoformat() if parsed_date else "Unrecognized"
    time = parsed_date.time().isoformat() if parsed_date else ""
    
    # Try to infer location from prepositions
    location = ""
    for word in text.split():
        if word.lower() in ["at", "in", "near", "on"]:
            index = text.lower().split().index(word)
            location = " ".join(text.split()[index + 1:index + 4])  # naive but usable
            break

    return {
        "status": "received",
        "title": title,
        "date": date,
        "time": time,
        "location": location,
        "description": text,
        "category": "general"
    }

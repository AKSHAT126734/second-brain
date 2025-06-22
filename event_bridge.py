import datetime

def handle_notion_event(payload):
    try:
        event_text = payload.get("text", "").lower()

        # Very basic parser (you can improve later)
        if "tomorrow" in event_text:
            event_date = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
        else:
            event_date = datetime.date.today()

        return {
            "status": "received",
            "title": event_text[:20] + "...",
            "date": str(event_date),
            "raw": event_text
        }

    except Exception as e:
        return {"error": str(e)}

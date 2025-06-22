import os
from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re

import dateparser  # NEW: handles natural language dates

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Notion Natural Language Event Bot is running!"

@app.route("/add-event", methods=["POST"])
def add_event():
    data = request.json
    event_text = data.get("event", "")

    # Step 1: Extract date and time
    parsed_date = dateparser.parse(event_text, settings={"PREFER_DATES_FROM": "future"})
    if not parsed_date:
        return jsonify({"error": "Could not detect a valid date/time."}), 400

    # Step 2: Try to extract known patterns (category, location, description)
    category_match = re.search(r"category:\s*([^\n,]+)", event_text, re.IGNORECASE)
    location_match = re.search(r"location:\s*([^\n,]+)", event_text, re.IGNORECASE)
    desc_match = re.search(r"description:\s*([^\n,]+)", event_text, re.IGNORECASE)

    category = category_match.group(1).strip() if category_match else "General"
    location = location_match.group(1).strip() if location_match else ""
    description = desc_match.group(1).strip() if desc_match else ""

    # Step 3: Remove known parts to guess the title
    cleaned = re.sub(r"(tomorrow|at\s*\d+.*?(am|pm))", "", event_text, flags=re.IGNORECASE)
    cleaned = re.sub(r"(category|location|description):\s*[^\n,]+", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip().capitalize()
    title_guess = cleaned if cleaned else "Untitled Event"

    # Step 4: Format date/time
    date_iso = parsed_date.isoformat()

    # Step 5: Build the Notion payload
    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Event": {
                "title": [{ "text": { "content": title_guess } }]
            },
            "Date": {
                "date": { "start": date_iso }
            },
            "Description": {
                "rich_text": [{ "text": { "content": description } }]
            },
            "Category": {
                "select": { "name": category }
            },
            "Location": {
                "rich_text": [{ "text": { "content": location } }]
            }
        }
    }

    res = requests.post("https://api.notion.com/v1/pages", json=payload, headers=headers)

    if res.status_code != 200:
        return jsonify({ "error": res.json() }), 400

    return jsonify({ "message": "✅ Event added!", "title": title_guess })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

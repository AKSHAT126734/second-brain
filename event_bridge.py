from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
import openai

# Load your OpenAI API key (you must set this in Render as an environment variable)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


class EventRequest(BaseModel):
    event: str


def chatgpt_parse_event(user_input: str) -> dict:
    system_prompt = """
You are a calendar assistant. Extract structured information from user messages.
Return a JSON object with the following fields:

- title: A short title for the event
- date: The date of the event in YYYY-MM-DD format
- time: The start time in 24-hour format (e.g., 16:00)
- location: The place of the event
- description: Full user input
- category: general, personal, health, work, etc. Choose best fit

If any field is missing or unknown, leave it as an empty string.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_input.strip()},
        ],
    )

    try:
        parsed_json = response['choices'][0]['message']['content']
        return eval(parsed_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")


def handle_notion_event(request: EventRequest):
    result = chatgpt_parse_event(request.event)
    result['status'] = "received"
    return result

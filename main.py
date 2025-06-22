from fastapi import FastAPI
from pydantic import BaseModel
from event_bridge import handle_notion_event

app = FastAPI()

class EventInput(BaseModel):
    event: str

@app.post("/notion-event")
async def receive_event(event_input: EventInput):
    result = handle_notion_event(event_input.event)
    return result

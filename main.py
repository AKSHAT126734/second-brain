from fastapi import FastAPI
from pydantic import BaseModel
from event_bridge import handle_notion_event

app = FastAPI()

# ✅ Step 1: Define a request body model
class NotionEvent(BaseModel):
    event: str

# ✅ Step 2: Use the model in your endpoint
@app.post("/notion-event")
async def receive_event(payload: NotionEvent):
    parsed = handle_notion_event(payload.event)
    return parsed

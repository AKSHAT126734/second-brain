from fastapi import FastAPI
from pydantic import BaseModel
from event_bridge import handle_notion_event

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Render-hosted app!"}

class EventRequest(BaseModel):
    event: str

@app.post("/notion-event")
def receive_event(payload: EventRequest):
    return handle_notion_event({"message": payload.event})

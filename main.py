from fastapi import FastAPI
from pydantic import BaseModel
from event_bridge import handle_notion_event

app = FastAPI()

# For browser check
@app.get("/")
def read_root():
    return {"message": "Hello from Render-hosted app!"}

# 📥 This is what powers the interactive /docs UI
class EventRequest(BaseModel):
    message: str

@app.post("/notion-event")
def create_event(request: EventRequest):
    return handle_notion_event({"event": request.message})

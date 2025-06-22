# main.py

from fastapi import FastAPI, Request
from event_bridge import handle_notion_event

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Render-hosted app!"}

@app.post("/notion-event")
async def receive_event(request: Request):
    payload = await request.json()
    return handle_notion_event(payload)

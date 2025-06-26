from fastapi import FastAPI, Request
from event_bridge import process_event

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "✅ Notion Sync API is running!"}

@app.post("/add-event")
async def add_event(request: Request):
    data = await request.json()
    return process_event(data)

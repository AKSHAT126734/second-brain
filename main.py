from fastapi import FastAPI, Request
from event_bridge import extract_event_details

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "✅ Notion Sync API is running!"}

@app.post("/add-event")
async def add_event(request: Request):
    payload = await request.json()
    message = payload.get("message") if isinstance(payload, dict) else str(payload)
    
    result = extract_event_details(message)
    return {
        "status": "success",
        "parsed_event": result
    }

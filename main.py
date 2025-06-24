from fastapi import FastAPI, Request
from event_bridge import handle_notion_event

app = FastAPI()

@app.post("/chatgpt-calendar")
async def chatgpt_calendar(request: Request):
    data = await request.json()
    return await handle_notion_event(data)

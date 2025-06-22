import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28"
}

res = requests.get(
    f"https://api.notion.com/v1/databases/{DATABASE_ID}",
    headers=headers
)

if res.status_code != 200:
    print("❌ Failed to fetch database schema:")
    print(res.text)
else:
    print("✅ Database Properties:\n")
    props = res.json()["properties"]
    for name, value in props.items():
        print(f"{name}: {value['type']}")

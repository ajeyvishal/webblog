import os

import requests
from dotenv import load_dotenv


load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
}


url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}"

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print(response.text)
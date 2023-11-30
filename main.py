from database_handler import NotionDatabaseHandler
from dotenv import load_dotenv
import os

load_dotenv("creds.env")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")
PAGE_ID = os.environ.get("PAGE_ID")

handler = NotionDatabaseHandler(notion_token=NOTION_TOKEN, database_id=DATABASE_ID, page_id=PAGE_ID)
handler.update_database({
    "Commits": 2,
    "PRs": 0,
    "Contributors": 1
})
result = handler.create_database()
print(result)
handler.populate_database(
    database_id=result['id'], 
    records=[
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino4"}}]}, "Commits": {"number": 6}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino3"}}]}, "Commits": {"number": 7}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino2"}}]}, "Commits": {"number": 8}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino1"}}]}, "Commits": {"number": 9}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino"}}]}, "Commits": {"number": 10}},
    ]
)
from database_handler import NotionDatabaseHandler
from dotenv import load_dotenv
import os

load_dotenv("creds.env")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")

handler = NotionDatabaseHandler(notion_token=NOTION_TOKEN, database_id=DATABASE_ID)
handler.update_database({
    "Commits": 2,
    "PRs": 0,
    "Contributors": 1
})
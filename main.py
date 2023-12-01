from database_handler import NotionDatabaseHandler
from overview_dashboard import GithubOverviewDashboard
from dotenv import load_dotenv
import os

load_dotenv("creds.env")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")
PAGE_ID = os.environ.get("PAGE_ID")

start_records = [
    {"Event": {"title": [{"type":"text", "text": {"content": "Contributors"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "PRs"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "Commits"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "Open Issues"}}]}, "Count": {"number": 0}}
]
dashboard = GithubOverviewDashboard(NOTION_TOKEN, parent_page_id=PAGE_ID)
dashboard.create_dashboard(start_records)

handler = NotionDatabaseHandler(NOTION_TOKEN, PAGE_ID)
result = handler.create_database("top_contributors.json")
handler.populate_database(
    database_id=result['database_id'], 
    records=[
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino4"}}]}, "Commits": {"number": 6}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino3"}}]}, "Commits": {"number": 7}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino2"}}]}, "Commits": {"number": 8}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino1"}}]}, "Commits": {"number": 9}},
        {"Name": {"title": [{"type":"text", "text": {"content": "gmguarino"}}]}, "Commits": {"number": 10}},
    ]
)
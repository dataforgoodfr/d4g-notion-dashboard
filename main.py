from dashboards.overview_dashboard import GithubOverviewDashboard
from dashboards.contributor_dashboard import GithubContributorsDashboard
from dotenv import load_dotenv
import os
import json

load_dotenv("creds.env")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
PAGE_ID = os.environ.get("PAGE_ID")

start_records = [
    {"Event": {"title": [{"type":"text", "text": {"content": "Contributors"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "PRs"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "Commits"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "Open Issues"}}]}, "Count": {"number": 0}}
]
dashboard = GithubOverviewDashboard(NOTION_TOKEN, parent_page_id=PAGE_ID)
dashboard.create_dashboard(start_records)
dashboard.update_dashboard(commits=1, pr=1, contributors=1)

contributor_dashboard = GithubContributorsDashboard(NOTION_TOKEN, PAGE_ID, n_contributors=5)

contributor_records = [
    {"Name": "gmguarino", "Commits": 10},
    {"Name": "gmguarino1", "Commits": 9},
    {"Name": "gmguarino2", "Commits": 8},
    {"Name": "gmguarino3", "Commits": 7},
]

database_id = contributor_dashboard.create_dashboard(contributor_dashboard.parse_contributors(contributor_records, as_records=True))

contributor_records = [
    {"Name": "ggg", "Commits": 10},
    {"Name": "ggg1", "Commits": 9},
    {"Name": "ggg2", "Commits": 8},
    {"Name": "ggg3", "Commits": 7},
]

print(contributor_dashboard.parse_contributors(contributor_records, as_records=True))
print(contributor_dashboard.parse_contributors(contributor_records, as_records=False))

contributor_dashboard.update_dashboard(contributor_dashboard.parse_contributors(contributor_records, as_records=False))
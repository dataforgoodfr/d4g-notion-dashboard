from dashboards.overview_dashboard import GithubOverviewDashboard
from dashboards.contributor_dashboard import GithubContributorsDashboard
from github_repo.github_handler import GithubHandler
from dotenv import load_dotenv
import os
import json

load_dotenv("creds.env")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
PAGE_ID = os.environ.get("PAGE_ID")


repo = GithubHandler(GITHUB_TOKEN, "org4g", "org4g-notion")
n_commits = repo.get_total_commits()
n_contributors = repo.get_total_contributors()
contributor_records = repo.get_top_contributors()
open_issues = repo.get_open_issues()

start_records = [
    {"Event": {"title": [{"type":"text", "text": {"content": "Contributors"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "PRs"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "Commits"}}]}, "Count": {"number": 0}},
    {"Event": {"title": [{"type":"text", "text": {"content": "Open Issues"}}]}, "Count": {"number": 0}}
]
dashboard = GithubOverviewDashboard(NOTION_TOKEN, parent_page_id=PAGE_ID)

# if the dashboard already exists it will just get the database_id for it
dashboard.create_dashboard(start_records)
# Updates with new values
dashboard.update_dashboard(commits=n_commits, pr=0, contributors=n_contributors, open_issues=open_issues)

contributor_dashboard = GithubContributorsDashboard(NOTION_TOKEN, PAGE_ID, n_contributors=5)

start_contributor_records = []

database_id = contributor_dashboard.create_dashboard(contributor_dashboard.parse_contributors(start_contributor_records, as_records=True))

print(contributor_dashboard.parse_contributors(contributor_records, as_records=True))
print(contributor_dashboard.parse_contributors(contributor_records, as_records=False))

contributor_dashboard.update_dashboard(contributor_dashboard.parse_contributors(contributor_records, as_records=False))
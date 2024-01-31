from dashboards.overview_dashboard import GithubOverviewDashboard
from dashboards.contributor_dashboard import GithubContributorsDashboard
from github_repo.github_handler import GithubHandler

import os
import json

import argparse


NOTION_TOKEN = os.environ.get("NOTION_DASHBOARD_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

print(os.environ)

def get_config(path):
    with open(path) as jf:
        config = json.load(jf)
    return config


def initialize_overview_dashboard(parent_page_id):
    start_records = [
        {"Event": {"title": [{"type":"text", "text": {"content": "Contributors"}}]}, "Count": {"number": 0}},
        {"Event": {"title": [{"type":"text", "text": {"content": "PRs"}}]}, "Count": {"number": 0}},
        {"Event": {"title": [{"type":"text", "text": {"content": "Commits"}}]}, "Count": {"number": 0}},
        {"Event": {"title": [{"type":"text", "text": {"content": "Open Issues"}}]}, "Count": {"number": 0}}
    ]
    
    dashboard = GithubOverviewDashboard(NOTION_TOKEN, parent_page_id=parent_page_id)
    # if the dashboard already exists it will just get the database_id for it
    dashboard.create_dashboard(start_records)
    return dashboard


def update_overview_dashboard(repo, dashboard):
    n_commits = repo.get_total_commits()
    n_contributors = repo.get_total_contributors()
    contributor_records = repo.get_top_contributors()
    open_issues = repo.get_open_issues()
    open_prs = repo.get_open_pull_requests()
    # Updates with new values
    dashboard.update_dashboard(commits=n_commits, pr=open_prs, contributors=n_contributors, open_issues=open_issues)


def initialize_contributor_dashboard(parent_page_id):
    start_records = []
    dashboard = GithubContributorsDashboard(NOTION_TOKEN, parent_page_id, n_contributors=5)
    # if the dashboard already exists it will just get the database_id for it
    dashboard.create_dashboard(dashboard.parse_contributors(start_records, as_records=True))
    return dashboard


def update_contributor_dashboard(repo, dashboard):
    contributor_records = repo.get_top_contributors()
    # Updates with new values
    dashboard.update_dashboard(dashboard.parse_contributors(contributor_records, as_records=False))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str)
    args = parser.parse_args()

    config = get_config(args.config)

    for project_group in config:
        for project in config[project_group]:
            print(project)
            repo = GithubHandler(GITHUB_TOKEN, project["github_org"], project["github_repo"])
            overview_dashboard = initialize_overview_dashboard(project["notion_page_id"])
            update_overview_dashboard(repo, overview_dashboard)

            contributor_dashboard = initialize_contributor_dashboard(project["notion_page_id"])
            update_contributor_dashboard(repo, contributor_dashboard)



# repo = GithubHandler(GITHUB_TOKEN, "org4g", "org4g-notion")
# n_commits = repo.get_total_commits()
# n_contributors = repo.get_total_contributors()
# contributor_records = repo.get_top_contributors()
# open_issues = repo.get_open_issues()
# open_prs = repo.get_open_pull_requests()

# start_records = [
#     {"Event": {"title": [{"type":"text", "text": {"content": "Contributors"}}]}, "Count": {"number": 0}},
#     {"Event": {"title": [{"type":"text", "text": {"content": "PRs"}}]}, "Count": {"number": 0}},
#     {"Event": {"title": [{"type":"text", "text": {"content": "Commits"}}]}, "Count": {"number": 0}},
#     {"Event": {"title": [{"type":"text", "text": {"content": "Open Issues"}}]}, "Count": {"number": 0}}
# ]
# dashboard = GithubOverviewDashboard(NOTION_TOKEN, parent_page_id=PAGE_ID)

# # if the dashboard already exists it will just get the database_id for it
# dashboard.create_dashboard(start_records)
# # Updates with new values
# dashboard.update_dashboard(commits=n_commits, pr=open_prs, contributors=n_contributors, open_issues=open_issues)

# contributor_dashboard = GithubContributorsDashboard(NOTION_TOKEN, PAGE_ID, n_contributors=5)

# start_contributor_records = []

# database_id = contributor_dashboard.create_dashboard(contributor_dashboard.parse_contributors(start_contributor_records, as_records=True))

# print(contributor_dashboard.parse_contributors(contributor_records, as_records=True))
# print(contributor_dashboard.parse_contributors(contributor_records, as_records=False))

# contributor_dashboard.update_dashboard(contributor_dashboard.parse_contributors(contributor_records, as_records=False))
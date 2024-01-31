from dashboards.overview_dashboard import GithubOverviewDashboard
from dashboards.contributor_dashboard import GithubContributorsDashboard
from github_repo.github_handler import GithubHandler

import os
import json

import argparse


# NOTION_TOKEN = os.environ.get("NOTION_DASHBOARD_TOKEN")
# GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

print(os.environ)

def get_config(path):
    with open(path) as jf:
        config = json.load(jf)
    return config


def initialize_overview_dashboard(args, parent_page_id):
    start_records = [
        {"Event": {"title": [{"type":"text", "text": {"content": "Contributors"}}]}, "Count": {"number": 0}},
        {"Event": {"title": [{"type":"text", "text": {"content": "PRs"}}]}, "Count": {"number": 0}},
        {"Event": {"title": [{"type":"text", "text": {"content": "Commits"}}]}, "Count": {"number": 0}},
        {"Event": {"title": [{"type":"text", "text": {"content": "Open Issues"}}]}, "Count": {"number": 0}}
    ]
    
    dashboard = GithubOverviewDashboard(args.notion_token, parent_page_id=parent_page_id)
    # dashboard = GithubOverviewDashboard(NOTION_TOKEN, parent_page_id=parent_page_id)
    # if the dashboard already exists it will just get the database_id for it
    dashboard.create_dashboard(start_records)
    return dashboard


def update_overview_dashboard(stats, dashboard):
    # Updates with new values
    dashboard.update_dashboard(commits=stats["n_commits"], pr=stats["open_prs"], contributors=stats["n_contributors"], open_issues=stats["open_issues"])


def get_overview_dashboard_stats(repo):
    n_commits = repo.get_total_commits()
    n_contributors = repo.get_total_contributors()
    open_issues = repo.get_open_issues()
    open_prs = repo.get_open_pull_requests()
    # Updates with new values
    return dict(n_commits=n_commits, n_contributors=n_contributors, open_issues=open_issues, open_prs=open_prs)


def update_repo_stats(overview_stats, repo_stats):
    for key in overview_stats:
        if key in repo_stats:
            repo_stats[key] = repo_stats[key] + overview_stats[key]
        else:
            repo_stats[key] = overview_stats[key]
    return repo_stats


def initialize_contributor_dashboard(args, parent_page_id):
    start_records = []
    dashboard = GithubContributorsDashboard(args.notion_token, parent_page_id, n_contributors=5)
    # if the dashboard already exists it will just get the database_id for it
    dashboard.create_dashboard(dashboard.parse_contributors(start_records, as_records=True))
    return dashboard

def get_contributor_dashboard_stats(repo):
    contributor_records = repo.get_top_contributors()
    # Updates with new values
    return contributor_records

def update_contributor_stats(contributor_stats, records):
    for record in records:
        if record["Name"] in contributor_stats:
            contributor_stats[record["Name"]] = contributor_stats[record["Name"]] + record["Commits"]
        else:
            contributor_stats[record["Name"]] = record["Commits"]
    return contributor_stats

def update_contributor_dashboard(contributor_stats, dashboard, n=10):
    contributor_records = [{"Name": key, "Commits": value} for key, value in contributor_stats.items()]
    contributor_records = sorted(contributor_records, key=lambda d: d['Commits'], reverse=True)[:n]
    # Updates with new values
    dashboard.update_dashboard(dashboard.parse_contributors(contributor_records, as_records=False))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str)
    parser.add_argument("--notion-token", type=str)
    parser.add_argument("--github-token", type=str)

    args = parser.parse_args()
    print("Got following args:")
    print(args)

    config = get_config(args.config)

    for project_group in config:
        contributor_stats = {}
        repo_stats = {}
        overview_dashboard = initialize_overview_dashboard(args, config[project_group]["notion_page_id"])
        contributor_dashboard = initialize_contributor_dashboard(args, config[project_group]["notion_page_id"])

        for project in config[project_group]["repos"]:
            repo = GithubHandler(args.github_token, project["github_org"], project["github_repo"])
            
            overview_stats = get_overview_dashboard_stats(repo)
            repo_stats = update_repo_stats(overview_stats, repo_stats)

            contributors = get_contributor_dashboard_stats(repo)
            contributor_stats = update_contributor_stats(contributor_stats, contributors)
        
        update_overview_dashboard(repo_stats, overview_dashboard)
        update_contributor_dashboard(contributor_stats, contributor_dashboard)



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
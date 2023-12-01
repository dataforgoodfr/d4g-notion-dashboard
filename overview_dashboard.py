from database_handler import NotionDatabaseHandler

class GithubOverviewDashboard(NotionDatabaseHandler):

    def __init__(self, notion_token, parent_page_id=None, database_id=None, template_dir="templates", template_file="overview.json") -> None:
        self.template_file = template_file
        super().__init__(notion_token, parent_page_id, database_id, template_dir)
    
    def create_dashboard(self, records):
        self.database_id = self.get_or_create_database(self.template_file, records)
        return self.database_id

    def update_dashboard(self, commits=0, pr=0, contributors=0):
        self.update_database_entries({
            "Commits": commits,
            "PRs": pr,
            "Contributors": contributors
        })

    
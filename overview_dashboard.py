from database_handler import NotionDatabaseHandler

class GithubOverviewDashboard(NotionDatabaseHandler):

    def __init__(self, notion_token, database_id=None, page_id=None, template_dir="templates", template_file="overview.json") -> None:
        self.template_file = template_file
        super().__init__(notion_token, database_id, page_id, template_dir)
    
    def create_dashboard(self):
        if self.database_id is None:
            self.database_id = self.create_database(self.template_file)['id']
            self.populate_database(
                database_id=self.database_id, 
                records=[
                    {"Event": {"title": [{"type":"text", "text": {"content": "Contributors"}}]}, "Commits": {"number": 0}},
                    {"Event": {"title": [{"type":"text", "text": {"content": "PRs"}}]}, "Commits": {"number": 0}},
                    {"Event": {"title": [{"type":"text", "text": {"content": "Commits"}}]}, "Commits": {"number": 0}},
                ]
            )
            
    def update_dashboard(self, commits=0, pr=0, contributors=0):
        self.update_database({
            "Commits": commits,
            "PRs": pr,
            "Contributors": contributors
        })

    
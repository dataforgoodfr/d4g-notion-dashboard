from .database_handler import NotionDatabaseHandler

class GithubContributorsDashboard(NotionDatabaseHandler):

    def __init__(self, notion_token, parent_page_id, n_contributors=10, database_id=None, template_dir="templates", template_file="top_contributors.json") -> None:
        self.template_file = template_file
        self.n_contributors = 10
        super().__init__(notion_token, parent_page_id, database_id, template_dir)
    
    def create_dashboard(self, records):
        self.database_id = self.get_or_create_database(self.template_file, records)
        return self.database_id
    
    def parse_contributors(self, pairs, as_records=True, reverse=False):
        if len(pairs) < self.n_contributors:
            padding = [{"Name": " ", "Commits": None}] * (self.n_contributors - len(pairs))
            pairs = pairs + padding
        elif len(pairs) >= self.n_contributors:
            pairs = pairs[:self.n_contributors]
        if reverse:
            pairs.reverse()
        records = []
        if as_records:
            for pair in pairs:
                records.append(
                    {"Name": {"title": [{"type":"text", "text": {"content": pair["Name"]}}]}, "Commits": {"number": pair["Commits"]}}
                )
            return records
        return pairs
    
    def update_dashboard(self, pairs):
        pages = self.get_pages()
        for pair, page in zip(pairs, pages):
            page["properties"]["Name"]["title"][0]["text"]["content"] = pair["Name"]
            page["properties"]["Commits"]["number"] = pair["Commits"]
            response = self.update_page(page)
            print(page["id"], response.status_code)

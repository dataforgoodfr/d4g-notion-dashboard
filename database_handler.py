from errors import KeyNotFoundError, IdNotSpecifiedError

import requests
import json
import os


class NotionDatabaseHandler(object):

    def __init__(self, notion_token, database_id=None, page_id=None, template_dir="templates") -> None:
        if database_id is None and page_id is None:
            raise IdNotSpecifiedError

        self.notion_token = notion_token
        self.database_id = database_id
        self.page_id = page_id
        self.template_dir = template_dir

        self.headers = {
            "Authorization": "Bearer " + self.notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def create_database(self):
        assert self.page_id is not None
        with open(os.path.join(self.template_dir, "top_contributors.json")) as jf:
            config = json.load(jf)
        config.update({
            "parent": {
                "type": "page_id",
                "page_id": self.page_id            }
        })
        url = "https://api.notion.com/v1/databases"
        response = requests.post(url, json=config, headers=self.headers)
        return response.json()
    
    def create_entry(self, database_id, entry: dict):
        create_url = "https://api.notion.com/v1/pages"

        payload = {"parent": {"database_id": database_id}, "properties": entry}

        res = requests.post(create_url, headers=self.headers, json=payload)
        return res

    def populate_database(self, database_id: str, records: dict):
        results = {}
        for entry in records:
            res = self.create_entry(database_id, entry)
            print(res.status_code)
            results.update(res.json())

    def get_pages(self, num_pages=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.headers)

        data = response.json()

        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
            response = requests.post(url, json=payload, headers=self.headers)
            data = response.json()
            results.extend(data["results"])

        return results


    def get_row_by_key(self, pages: list, key: str):
        for page in pages:
            if page["object"] == "page" and page["properties"]["Name"]["title"][0]["text"]["content"] == key:
                return page
        raise KeyNotFoundError(key=key)


    def update_value(self, page, new_value):
        page["properties"]["Number"]["number"] = new_value
        return page


    def update_page(self, page):
        page_id = page["id"]
        data = page["properties"]
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"properties": data}
        res = requests.patch(url, json=payload, headers=self.headers)
        return res
    

    def update_database(self, config: dict):
        pages = self.get_pages()
        for key, value in config.items():
            page = self.get_row_by_key(pages, key=key)
            page = self.update_value(page, value)
            res = self.update_page(page)
            print(res.status_code)
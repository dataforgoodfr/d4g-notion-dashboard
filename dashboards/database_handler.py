from .errors import KeyNotFoundError, IdNotSpecifiedError, TemplateNotSpecifiedError

from time import sleep
import requests
import json
import os


class NotionDatabaseHandler(object):
    """
    General class to handle the connection to a Notion Database.
    """
    def __init__(self, notion_token, parent_page_id=None, database_id=None, template_dir="templates") -> None:
        if database_id is None and parent_page_id is None:
            raise IdNotSpecifiedError

        self.notion_token = notion_token
        self.database_id = database_id
        self.parent_page_id = parent_page_id
        self.template_dir = template_dir

        self.headers = {
            "Authorization": "Bearer " + self.notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def create_database(self, template_file=None, json_template=None):
        """
        Creates the database from a json template file and the parent page id
        """
        assert self.parent_page_id is not None

        if json_template is not None:
            config = json_template
        elif template_file is not None:
            with open(os.path.join(self.template_dir, template_file)) as jf:
                config = json.load(jf)
        else:
            raise TemplateNotSpecifiedError

        config.update({
            "parent": {
                "type": "page_id",
                "page_id": self.parent_page_id
            }
        })
        url = "https://api.notion.com/v1/databases"
        response = requests.post(url, json=config, headers=self.headers)
        return {"database_id": response.json()['id']}
    
    def create_entry(self, database_id, entry: dict):
        """
        Creates an entry in the database given a database id and a record
        """
        create_url = "https://api.notion.com/v1/pages"

        payload = {"parent": {"database_id": database_id}, "properties": entry}

        res = requests.post(create_url, headers=self.headers, json=payload)
        return res

    def populate_database(self, database_id: str, records: list):
        """
        Populates a database with a list of records
        """
        results = {}
        for entry in records:
            
            res = self.create_entry(database_id, entry)
            print(res.json())
            results.update(res.json())
            sleep(0.4)

    def get_pages(self, num_pages=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        Here pages, are the individual entries in the database, following the 
        Notion notation (no pun intended).
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


    def get_row_by_key(self, pages: list, key: str, column_name:str="Event"):
        """
        Gets the entry in the Database searching the specific key.
        There is probably a more efficient way to do this.
        """
        for page in pages:
            print(page["properties"])
            if page["object"] == "page" and page["properties"][column_name]["title"][0]["text"]["content"] == key:
                return page
        raise KeyNotFoundError(key=key)


    def update_numerical_value(self, page, new_value, column_name="Count"):
        "Updates the Numerical value"
        page["properties"][column_name]["number"] = new_value
        return page
    
    def update_title_key(self, page, text, column_name="Event"):
        """
        Changes the name of the entry key.
        """
        page["properties"][column_name]["title"][0]["text"]["content"] = text
        return page

    def update_page(self, page):
        """
        Updates a page. A page here is a database entry.
        """
        page_id = page["id"]
        data = page["properties"]
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"properties": data}
        res = requests.patch(url, json=payload, headers=self.headers)
        return res
    
    def update_database_entries(self, config: dict):
        """
        Updates the entries in the database using key/value pairs
        """
        pages = self.get_pages()
        for key, value in config.items():
            page = self.get_row_by_key(pages, key=key)
            page = self.update_numerical_value(page, value)
            res = self.update_page(page)
            print(res.status_code)

    def update_database_complete(self, config: dict):
        pages = self.get_pages()
        # TODO
        pass

    def search_database_by_title(self, title:str):
        """
        Searches for a database with the specified title associated with the 
        parent page id
        """
        payload = {
            "query":f"{title}",
            "filter": {
                "value": "database",
                "property": "object"
            },
            "sort":{
                "direction":"ascending",
                "timestamp":"last_edited_time"
            }
        }

        search_url = "https://api.notion.com/v1/search"

        response = requests.post(search_url, headers=self.headers, json=payload)
        data = response.json()
        results = data["results"]
        while data["has_more"]:
            payload = {"page_size": 100, "start_cursor": data["next_cursor"]}
            response = requests.post(search_url, json=payload, headers=self.headers)
            data = response.json()
            results.extend(data["results"])

        for result in results:
            if result["parent"]["type"] == "page_id":
                if result["parent"]["page_id"] == os.environ.get("PAGE_ID") and result["archived"] is False:
                    print(result['id'], result["title"][0]["text"]["content"])
                    return {"database_id": result["id"]}

        return {"database_id": None}
    
    def get_or_create_database(self, template_file, records):
        with open(os.path.join(self.template_dir, template_file)) as jf:
            config = json.load(jf)
        title = config["title"][0]["text"]["content"]
        self.database_id = self.search_database_by_title(title)['database_id']
        if self.database_id is None:
            self.database_id = self.create_database(json_template=config)["database_id"]
            self.populate_database(
                database_id=self.database_id, 
                records=records
            )
        return self.database_id



if __name__=="__main__":
    # Testing the search API
    from dotenv import load_dotenv

    load_dotenv("creds.env")

    NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    data = {
        "query":"Repository Activity",
        "filter": {
            "value": "database",
            "property": "object"
        },
        "sort":{
            "direction":"ascending",
            "timestamp":"last_edited_time"
        }
    }

    response = requests.post("https://api.notion.com/v1/search", headers=headers, json=data)
    for result in response.json()['results']:
        if result["parent"]["type"] == "page_id":
            if result["parent"]["page_id"] == os.environ.get("PAGE_ID"):
                print(result['id'], result["title"][0]["text"]["content"])

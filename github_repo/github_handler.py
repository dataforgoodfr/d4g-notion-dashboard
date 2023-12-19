import requests
import json
from time import sleep


class GithubNoContentError(Exception):
    """Exception raised when getting a header with no content from a Github API call
    """

    def __init__(self, response):
        message = f"The query produced a header with no response and status code {response.status_code}."
        super().__init__(message)     


class GithubNotFoundError(Exception):
    """Exception raised when a resource is not found during a Github API call
    """

    def __init__(self, response):
        message = f"The required resource was not found: {response.status_code}."
        super().__init__(message)


class GithubGenericError(Exception):
    """Exception raised for a generic error during a Github API call
    """

    def __init__(self, response):
        message = f"Generic error was returned with status code: {response.status_code}."
        super().__init__(message)     


class GithubHandler(object):

    def __init__(self, github_token, github_owner, github_repo):
        self.__dict__.update({key:val for key,val in vars().items() if key!="self"})
        self.headers = {
            "Authorization": "Bearer " + github_token,
            "Content-Type": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def __parse_error_code(self, response):
        if response.status_code == 204:
            raise GithubNoContentError(response)
        elif response.status_code == 404:
            raise GithubNotFoundError(response)
        else:
            raise GithubGenericError(response)

    def __get_request_generic(self, request_url):
            response = requests.get(url=request_url, headers=self.headers)
            while response.status_code == 202:
                sleep(1)
                response = requests.get(url=request_url, headers=self.headers)
            if response.status_code == 200:
                return response
            else:
                self.__parse_error_code(response)

    
    def get_total_commits(self):

        request_url=f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/commits"
        response = self.__get_request_generic(request_url)
        return len(response.json())
    
    def get_total_contributors(self):
        request_url=f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/stats/contributors"
        response = self.__get_request_generic(request_url)
        return len(response.json())
    
    def get_top_contributors(self, n=10):
        request_url=f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/stats/contributors"
        response = self.__get_request_generic(request_url)
        data = response.json()
        contributor_records = list(map(lambda d: {"Name": d["author"]["login"], "Commits": d["total"]}, data))
        contributor_records = sorted(contributor_records, key=lambda d: d['Commits'], reverse=True)[:n]
        return contributor_records

        
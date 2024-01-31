class KeyNotFoundError(Exception):
    """Exception raised for errors in finding the dashboard key.

    Attributes:
        key -- input key which caused the error
    """

    def __init__(self, key):
        message = f"Cannot find specified key ({key}) in any of the pages. Check spelling and remember serach is case sensitive."
        super().__init__(message)


class RequestNotSuccessfulError(Exception):
    """Exception raised if results are not present in notion POST API call.

    Attributes:
        data -- the returned data
    """

    def __init__(self, data):
        message = f"The API call was not successful. Expected 'results' in json body got: \n{data}"
        super().__init__(message)


class IdNotSpecifiedError(Exception):
    """Exception raised for not specifying either page id or the database id.
    """

    def __init__(self):
        message = "Please provide either a database ID or a page id where the database can be created."
        super().__init__(message)


class TemplateNotSpecifiedError(Exception):
    """Exception raised for not specifying a template for the database to be created
    """

    def __init__(self):
        message = "Please provide a template for the database or a template filepath."
        super().__init__(message)       
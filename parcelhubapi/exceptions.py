"""Exceptions for the parcelhubapi package."""


class LoginCredentialsNotSetError(ValueError):
    """Exception raised when creating an API session without credentials set."""

    def __init__(self, *args, **kwargs):
        """Exception raised when creating an API session without credentials set."""
        super().__init__("USERNAME, PASSWORD and ACCOUNT_ID must be set.")


class ResponseParsingError(ValueError):
    """Exception raised when there is an error parsing an API response."""

    def __init__(self, response_text, *args, **kwargs):
        """Exception raised when there is an error parsing an API response."""
        super().__init__(f"Error parsing response: {response_text!r}.")


class ResponseStatusError(ValueError):
    """Exception raised when a response has an error status."""

    def __init__(self, response, *args, **kwargs):
        """Exception raised when a response has an error status."""
        super().__init__(f"Error response ({response.status_code}): {response.text!r}.")

"""Exceptions for the parcelhupapi package."""

from pathlib import Path

import toml

from . import exceptions
from .request import GetTokenRequest


class ParcelhubAPISession:
    """Session manager for parcelhubapi."""

    LIVE_DOMAIN = "https://api.parcelhub.net"
    TEST_DOMAIN = "https://api.test.parcelhub.net"

    NSMAP = {
        "xsd": "http://www.w3.org/2001/XMLSchema",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        None: "http://api.parcelhub.net/schemas/api/parcelhub-api-v0.4.xsd",
    }

    DOMAIN = LIVE_DOMAIN

    CONFIG_FILENAME = ".parcelhubapi.toml"

    username = None
    password = None
    account_id = None

    access_token = None
    refresh_token = None

    def __enter__(self):
        if not self.credentials_are_set():
            self.load_from_config_file()
            if not self.credentials_are_set():
                raise exceptions.LoginCredentialsNotSetError()
        try:
            self.authorise_session()
        except Exception:
            raise
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __init__(self, username=None, password=None, account_id=None):
        """Create a Parcelhub API session."""
        self.username = username
        self.password = password
        self.account_id = account_id

    def credentials_are_set(self):
        """Return True if all auth credentials are set, otherwise False."""
        if None in (self.username, self.password, self.account_id):
            return False
        else:
            return True

    def find_config_filepath(self):
        """
        Return the path to a shopify config file or None.

        Recursivly scan backwards from the current working directory and return the
        path to a file matching self.CONFIG_FILENAME if one exists, otherwise returns
        None.
        """
        if self.CONFIG_FILENAME is None:
            return None
        path = Path.cwd()
        while path.parent != path:
            config_file = path / self.CONFIG_FILENAME
            if config_file.exists():
                return config_file
            path = path.parent
        return None

    def load_from_config_file(self, config_file_path=None):
        """Set login credentials as specified in a toml file located at config_file_path."""
        if config_file_path is None:
            config_file_path = self.find_config_filepath()
        with open(config_file_path) as f:
            config = toml.load(f)
        self.username = config.get("USERNAME")
        self.password = config.get("PASSWORD")
        self.account_id = config.get("ACCOUNT_ID")

    def authorise_session(self):
        """Request access token and refresh token."""
        request = GetTokenRequest(self)
        self.access_token, self.refresh_token = request.call()

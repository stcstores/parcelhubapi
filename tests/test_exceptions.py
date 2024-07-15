import re
from unittest import mock

import pytest

from parcelhubapi import exceptions


def test_login_credentials_not_set_error():
    with pytest.raises(
        exceptions.LoginCredentialsNotSetError,
        match=re.escape("USERNAME, PASSWORD and ACCOUNT_ID must be set."),
    ):
        raise exceptions.LoginCredentialsNotSetError


def test_response_parsing_error():
    response_text = "Invalid Response"
    with pytest.raises(
        exceptions.ResponseParsingError,
        match=re.escape('Error parsing response: "Invalid Response".'),
    ):
        raise exceptions.ResponseParsingError(response_text)


def test_response_status_error():
    response = mock.Mock(status_code=500, text="Invalid Response")
    with pytest.raises(
        exceptions.ResponseStatusError,
        match=re.escape('Error response (500): "Invalid Response".'),
    ):
        raise exceptions.ResponseStatusError(response)

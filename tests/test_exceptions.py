import pytest

from parcelhubapi import exceptions


def test_login_credentials_not_set_error():
    with pytest.raises(
        exceptions.LoginCredentialsNotSetError,
        match="USERNAME, PASSWORD and ACCOUNT_ID must be set.",
    ):
        raise exceptions.LoginCredentialsNotSetError


def test_response_parsing_error():
    response_text = "Invalid Response"
    with pytest.raises(
        exceptions.ResponseParsingError,
        match='Error parsing response: "Invalid Response".',
    ):
        raise exceptions.ResponseParsingError(response_text)

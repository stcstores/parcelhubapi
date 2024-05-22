import pytest

from parcelhubapi import exceptions


def test_login_credentials_not_set_error():
    with pytest.raises(
        exceptions.LoginCredentialsNotSetError,
        match="USERNAME, PASSWORD and ACCOUNT_ID must be set.",
    ):
        raise exceptions.LoginCredentialsNotSetError

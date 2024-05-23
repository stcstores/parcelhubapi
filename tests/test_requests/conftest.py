from unittest import mock

import pytest


@pytest.fixture
def request_args():
    return ["a", "b"]


@pytest.fixture
def request_kwargs():
    return {"1": 1, "2": 2}


@pytest.fixture
def domain():
    return "https://api.test.com"


@pytest.fixture
def access_token():
    return "test-access-token-string"


@pytest.fixture
def refresh_token():
    return "test-refresh-token-string"


@pytest.fixture
def username():
    return "TEST_USERNAME"


@pytest.fixture
def password():
    return "TEST_PASSWORD"


@pytest.fixture
def account_id():
    return "TEST_ACCOUNT_ID"


@pytest.fixture
def mock_session(domain, access_token, username, password, account_id):
    return mock.Mock(
        DOMAIN=domain,
        access_token=access_token,
        username=username,
        password=password,
        account_id=account_id,
    )

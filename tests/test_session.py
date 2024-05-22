from unittest import mock

import pytest
import toml

from parcelhubapi import exceptions
from parcelhubapi.session import ParcelhubAPISession


@pytest.fixture(autouse=True)
def temp_cwd(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


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
def access_token():
    return "lshgoisdhgosdoisdfsdnfljksdhgoishnfgosdjipdgsowe"


@pytest.fixture
def refresh_token():
    return "lshgoisdhgosdoisdfsdnfljksdhgoishnfgosdjipdgsowe"


@pytest.fixture
def config_filename():
    return "config_file.toml"


@pytest.fixture
def config_file(temp_cwd, config_filename, username, password, account_id):
    data = {"USERNAME": username, "PASSWORD": password, "ACCOUNT_ID": account_id}
    path = temp_cwd / config_filename
    with open(path, "w") as f:
        toml.dump(data, f)
    return path


@pytest.fixture
def mock_credentials_are_set_method():
    with mock.patch(
        "parcelhubapi.session.ParcelhubAPISession.credentials_are_set"
    ) as m:
        m.return_value = True
        yield m


@pytest.fixture
def mock_load_from_config_file_method():
    with mock.patch(
        "parcelhubapi.session.ParcelhubAPISession.load_from_config_file"
    ) as m:
        yield m


@pytest.fixture
def mock_find_config_filepath_method():
    with mock.patch(
        "parcelhubapi.session.ParcelhubAPISession.find_config_filepath"
    ) as m:
        yield m


@pytest.fixture
def mock_authorise_session_method():
    with mock.patch("parcelhubapi.session.ParcelhubAPISession.authorise_session") as m:
        yield m


@pytest.fixture
def mock_get_token_request(access_token, refresh_token):
    with mock.patch("parcelhubapi.session.GetTokenRequest") as m:
        m.return_value.call.return_value = (access_token, refresh_token)
        yield m


def test_init_sets_passed_credentials(username, password, account_id):
    session = ParcelhubAPISession(
        username=username, password=password, account_id=account_id
    )
    assert session.username == username
    assert session.password == password
    assert session.account_id == account_id


def test_enter_method_with_credentials_set(
    username,
    password,
    account_id,
    mock_credentials_are_set_method,
    mock_find_config_filepath_method,
    mock_authorise_session_method,
):
    with ParcelhubAPISession(
        username=username, password=password, account_id=account_id
    ):
        pass
    mock_credentials_are_set_method.call_count == 1
    mock_find_config_filepath_method.assert_not_called()
    mock_authorise_session_method.assert_called_once_with()


def test_enter_method_with_load_credentials_from_file(
    username,
    password,
    account_id,
    mock_authorise_session_method,
    mock_credentials_are_set_method,
    mock_load_from_config_file_method,
):
    mock_credentials_are_set_method.side_effect = [False, True]
    with ParcelhubAPISession():
        pass
    mock_credentials_are_set_method.call_count == 2
    mock_load_from_config_file_method.assert_called_once_with()
    mock_authorise_session_method.assert_called_once_with()


def test_enter_method_without_config_or_path(
    mock_credentials_are_set_method,
    mock_load_from_config_file_method,
    mock_find_config_filepath_method,
    mock_authorise_session_method,
):
    mock_credentials_are_set_method.side_effect = [False, False]
    mock_find_config_filepath_method.return_value = None
    with pytest.raises(exceptions.LoginCredentialsNotSetError):
        with ParcelhubAPISession():
            pass
    mock_credentials_are_set_method.call_count == 2
    mock_authorise_session_method.assert_not_called()


def test_enter_method_with_get_token_request_error(
    mock_credentials_are_set_method,
    mock_load_from_config_file_method,
    mock_find_config_filepath_method,
    mock_authorise_session_method,
):
    mock_authorise_session_method.side_effect = Exception
    with pytest.raises(Exception):
        with ParcelhubAPISession():
            pass
    mock_authorise_session_method.assert_called_once_with()


@pytest.mark.parametrize(
    "username,password,account_id,expected",
    (
        ("TEST_USERNAME", "TEST_PASSWORD", "TEST_ACCOUNT_ID", True),
        (None, "TEST_PASSWORD", "TEST_ACCOUNT_ID", False),
        ("TEST_USERNAME", None, "TEST_ACCOUNT_ID", False),
        ("TEST_USERNAME", "TEST_PASSWORD", None, False),
        (None, None, "TEST_ACCOUNT_ID", False),
        (None, None, None, False),
    ),
)
def test_credentials_are_set_method(
    username, password, account_id, expected, mock_get_token_request
):
    session = ParcelhubAPISession(
        username=username, password=password, account_id=account_id
    )
    assert session.credentials_are_set() is expected


def test_find_config_filepath_returns_config_file_in_cwd(
    temp_cwd, mock_get_token_request, config_filename, config_file
):
    session = ParcelhubAPISession()
    session.CONFIG_FILENAME = config_filename
    path = session.find_config_filepath()
    assert path == temp_cwd / session.CONFIG_FILENAME


def test_find_config_filepath_returns_none_without_config_file_path_set():
    session = ParcelhubAPISession()
    session.CONFIG_FILENAME = None
    path = session.find_config_filepath()
    assert path is None


def test_find_config_filepath_returns_None_without_config_file_in_cwd(
    mock_get_token_request, config_filename
):
    session = ParcelhubAPISession()
    session.CONFIG_FILENAME = config_filename
    path = session.find_config_filepath()
    assert path is None


def test_load_from_config_file_method(config_file, username, password, account_id):
    session = ParcelhubAPISession()
    session.load_from_config_file(config_file)
    assert session.username == username
    assert session.password == password
    assert session.account_id == account_id


def test_load_from_config_file_method_without_passing_path(
    config_filename, config_file, username, password, account_id
):
    session = ParcelhubAPISession()
    session.CONFIG_FILENAME = config_filename
    session.load_from_config_file()
    assert session.username == username
    assert session.password == password
    assert session.account_id == account_id


def test_authorise_session_method(mock_get_token_request, access_token, refresh_token):
    session = ParcelhubAPISession()
    session.authorise_session()
    mock_get_token_request.assert_called_once_with(session)
    mock_get_token_request.return_value.call.assert_called_once_with()
    assert session.access_token == access_token
    assert session.refresh_token == refresh_token

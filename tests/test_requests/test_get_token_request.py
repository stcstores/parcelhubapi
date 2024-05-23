from unittest import mock

import pytest

from parcelhubapi.request import BaseParcelhubApiRequest, GetTokenRequest


@pytest.fixture
def request_obj(mock_session):
    return GetTokenRequest(session=mock_session)


def test_url_attribute(request_obj):
    assert request_obj.URL == "1.0/TokenV2"


def test_method_attribute(request_obj):
    assert request_obj.METHOD == BaseParcelhubApiRequest.POST


def test_init_method(mock_session, request_obj):
    assert request_obj.session == mock_session


def test_url_method(mock_session, request_obj):
    request_obj = GetTokenRequest(mock_session)
    assert request_obj.url() == "https://api.test.com/1.0/TokenV2"


def test_headers_method(request_obj):
    expected = {
        "Content-type": "application/xml; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
    }
    assert request_obj.headers() == expected


def test_params_method(request_obj):
    assert request_obj.params() is None


def test_data_method(request_obj):
    expected = (
        "<?xml version='1.0' encoding='utf-8'?>\n<RequestToken "
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
        "<grant_type>bearer</grant_type>"
        "<username>TEST_USERNAME</username>"
        "<password>TEST_PASSWORD</password>"
        "</RequestToken>"
    )
    assert request_obj.data().decode("utf-8") == expected


def test_parse_response_method(request_obj, refresh_token, access_token):
    response_text = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<TokenV2 xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<refreshToken>{refresh_token}</refreshToken>"
        f"<access_token>{access_token}</access_token>"
        "<expiresIn>14400</expiresIn>"
        "</TokenV2>"
    )
    response = mock.Mock(text=response_text)
    assert request_obj.parse_response(response) == (access_token, refresh_token)


@mock.patch("parcelhubapi.request.requests")
def test_call_method(mock_requests, request_args, request_kwargs, request_obj):
    request_obj.url = mock.Mock()
    request_obj.headers = mock.Mock()
    request_obj.params = mock.Mock()
    request_obj.data = mock.Mock()
    request_obj.parse_response = mock.Mock()
    value = request_obj.call(*request_args, **request_kwargs)
    request_obj.url.assert_called_once_with(*request_args, **request_kwargs)
    request_obj.headers.assert_called_once_with(*request_args, **request_kwargs)
    request_obj.params.assert_called_once_with(*request_args, **request_kwargs)
    request_obj.data.assert_called_once_with(*request_args, **request_kwargs)
    mock_requests.request.assert_called_once_with(
        url=request_obj.url.return_value,
        method=request_obj.METHOD,
        headers=request_obj.headers.return_value,
        params=request_obj.params.return_value,
        data=request_obj.data.return_value,
    )
    mock_requests.request.return_value.raise_for_status.assert_called_once_with()
    request_obj.parse_response.assert_called_once_with(
        mock_requests.request.return_value, *request_args, **request_kwargs
    )
    assert value == request_obj.parse_response.return_value

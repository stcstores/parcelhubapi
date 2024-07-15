import re
from unittest import mock

import pytest
from requests import Response

from parcelhubapi import exceptions
from parcelhubapi.request import BaseParcelhubApiRequest


@pytest.fixture
def request_obj(mock_session):
    return BaseParcelhubApiRequest(session=mock_session)


def test_get_constant():
    assert BaseParcelhubApiRequest.GET == "GET"


def test_post_constant():
    assert BaseParcelhubApiRequest.POST == "POST"


def test_url_attribute(request_obj):
    assert request_obj.URL == ""


def test_method_attribute(request_obj):
    assert request_obj.METHOD == BaseParcelhubApiRequest.GET


def test_init_method(mock_session, request_obj):
    assert request_obj.session == mock_session


def test_url_method(mock_session, request_obj):
    request_obj = BaseParcelhubApiRequest(mock_session)
    request_obj.URL = "endpoint"
    assert request_obj.url() == "https://api.test.com/endpoint"


def test_headers_method(access_token, request_obj):
    expected = {
        "Content-type": "application/xml; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Authorization": f"bearer {access_token}",
    }
    assert request_obj.headers() == expected


def test_params_method(request_obj):
    assert request_obj.params() is None


def test_data_method(request_obj):
    assert request_obj.data() is None


def test_parse_response_method(request_obj):
    response = mock.Mock()
    assert request_obj.parse_response(response) == response.text


@mock.patch("parcelhubapi.request.requests")
def test_call_method(mock_requests, request_args, request_kwargs, request_obj):
    request_obj.url = mock.Mock()
    request_obj.headers = mock.Mock()
    request_obj.params = mock.Mock()
    request_obj.data = mock.Mock()
    request_obj.check_response = mock.Mock()
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
    request_obj.check_response.assert_called_once_with(
        mock_requests.request.return_value
    )
    request_obj.parse_response.assert_called_once_with(
        mock_requests.request.return_value, *request_args, **request_kwargs
    )
    assert value == request_obj.parse_response.return_value


def test_check_response_method(request_obj):
    response = mock.Mock()
    request_obj.check_response(response)
    response.raise_for_status.assert_called_once_with()


def test_check_response_method_handles_error(request_obj):
    response = mock.Mock()
    response.raise_for_status.side_effect = Exception
    with pytest.raises(Exception):
        request_obj.check_response(response)
    response.raise_for_status.assert_called_once_with()


def test_check_response_method_handles_raise_for_status(request_obj):
    response = Response()
    response._content = b"Invalid Response"
    response.status_code = 500
    with pytest.raises(
        exceptions.ResponseStatusError,
        match=re.escape('Error response (500): "Invalid Response".'),
    ):
        request_obj.check_response(response)

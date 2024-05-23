from unittest import mock

import pytest

from parcelhubapi.request import BaseParcelhubApiRequest, GetDraftShipmentsRequest


@pytest.fixture
def request_obj(mock_session):
    return GetDraftShipmentsRequest(session=mock_session)


def test_url_attribute(request_obj):
    assert request_obj.URL == "1.0/DraftShipment"


def test_method_attribute(request_obj):
    assert request_obj.METHOD == BaseParcelhubApiRequest.GET


def test_init_method(mock_session, request_obj):
    assert request_obj.session == mock_session


def test_url_method(mock_session, request_obj):
    request_obj = GetDraftShipmentsRequest(mock_session)
    assert request_obj.url() == "https://api.test.com/1.0/DraftShipment"


def test_headers_method(access_token, request_obj):
    expected = {
        "Content-type": "application/xml; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Authorization": f"bearer {access_token}",
    }
    assert request_obj.headers() == expected


def test_params_method(request_obj, account_id):
    assert request_obj.params() == {"AccountId": account_id}


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

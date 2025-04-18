from pathlib import Path
from unittest import mock

import pytest

from parcelhubapi.exceptions import ResponseParsingError
from parcelhubapi.models import CreateShipmentResponse
from parcelhubapi.request import BaseParcelhubApiRequest, CreateDraftShipmentRequest


@pytest.fixture
def request_obj(mock_session):
    return CreateDraftShipmentRequest(session=mock_session)


@pytest.fixture
def shipment_request_data():
    return mock.Mock()


@pytest.fixture
def response_text():
    with open(Path(__file__).parent / "shipment_response.xml") as f:
        return f.read()


def test_url_attribute(request_obj):
    assert request_obj.URL == "1.0/DraftShipment"


def test_method_attribute(request_obj):
    assert request_obj.METHOD == BaseParcelhubApiRequest.POST


def test_init_method(mock_session, request_obj):
    assert request_obj.session == mock_session


def test_url_method(mock_session, request_obj):
    request_obj = CreateDraftShipmentRequest(mock_session)
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
    assert request_obj.params() == {
        "AccountId": account_id,
        "RequestedLabelFormat": "ZPL",
        "RequestedLabelSize": 6,
    }


@mock.patch("parcelhubapi.request.etree")
def test_data_method(mock_etree, request_obj, shipment_request_data):
    value = request_obj.data(shipment_request=shipment_request_data)
    shipment_request_data.as_xml.assert_called_once_with()
    mock_etree.tostring.assert_called_once_with(
        shipment_request_data.as_xml.return_value,
        encoding="utf-8",
        xml_declaration=True,
    )
    assert value == mock_etree.tostring.return_value


def test_parse_response_method(request_obj, response_text):
    response = mock.Mock(text=response_text)
    value = request_obj.parse_response(response)
    assert isinstance(value, CreateShipmentResponse)
    assert value.shipment_id == "14074848347197107"
    assert value.courier_tracking_number == "1ZC7V9230433575084"
    assert value.parcelhub_tracking_number == "WHL0P050000036532"


def test_parse_response_method_with_error(request_obj, response_text):
    response = mock.Mock(text="Some Invalid Text")
    with pytest.raises(
        ResponseParsingError, match="Error parsing response: 'Some Invalid Text'."
    ):
        request_obj.parse_response(response)


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

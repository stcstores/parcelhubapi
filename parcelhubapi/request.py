"""Parcelhub API requests."""

import sys

import requests
from lxml import etree

from . import exceptions
from .models import CreateShipmentResponse


class BaseParcelhubApiRequest:
    """Base class for Parcelhhub requests."""

    URL = ""

    GET = "GET"
    POST = "POST"

    METHOD = GET

    def __init__(self, session):
        """Set request session."""
        self.session = session

    def url(self, *args, **kwargs):
        """Return the request URL."""
        return f"{self.session.DOMAIN}/{self.URL}"

    def headers(self, *args, **kwargs):
        """Return request headers."""
        return {
            "Content-type": "application/xml; charset=utf-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Authorization": f"bearer {self.session.access_token}",
        }

    def params(self, *args, **kwargs):
        """Return request params."""
        return None

    def data(self, *args, **kwargs):
        """Return request data."""
        return None

    def parse_response(self, response, *args, **kwargs):
        """Parse the request response."""
        return response.text

    def call(self, *args, **kwargs):
        """Make an API request."""
        response = requests.request(
            url=self.url(*args, **kwargs),
            method=self.METHOD,
            headers=self.headers(*args, **kwargs),
            params=self.params(*args, **kwargs),
            data=self.data(*args, **kwargs),
        )
        self.check_response(response)
        return self.parse_response(response, *args, **kwargs)

    def check_response(self, response):
        """Check the response status code."""
        try:
            response.raise_for_status()
        except Exception:
            raise exceptions.ResponseStatusError(response)
            print(response.text, file=sys.stderr)
            raise


class GetTokenRequest(BaseParcelhubApiRequest):
    """Request for getting a refresh token and access token."""

    URL = "1.0/TokenV2"
    METHOD = BaseParcelhubApiRequest.POST

    GRANT_TYPE = "grant_type"
    USERNAME = "username"
    PASSWORD = "password"

    BARER = "bearer"

    NSMAP = {
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsd": "http://www.w3.org/2001/XMLSchema",
    }

    def headers(self, *args, **kwargs):
        """Return request headers."""
        return {
            "Content-type": "application/xml; charset=utf-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
        }

    def data(self, *args, **kwargs):
        """Return the request body."""
        root = etree.Element("RequestToken", nsmap=self.NSMAP)
        etree.SubElement(root, self.GRANT_TYPE).text = self.BARER
        etree.SubElement(root, self.USERNAME).text = self.session.username
        etree.SubElement(root, self.PASSWORD).text = self.session.password
        return etree.tostring(root, encoding="utf-8", xml_declaration=True)

    def parse_response(self, response, *args, **kwargs):
        """Return access token and refresh token."""
        root = etree.XML(response.text[38:])
        refresh_token = root.find("refreshToken").text
        access_token = root.find("access_token").text
        return access_token, refresh_token


class GetShipmentsRequest(BaseParcelhubApiRequest):
    """Request for retrieving active shipments."""

    URL = "1.0/Shipment"
    METHOD = BaseParcelhubApiRequest.GET

    def params(self, *args, **kwargs):
        """Return request parameters."""
        return {"AccountId": self.session.account_id}


class GetDraftShipmentsRequest(GetShipmentsRequest):
    """Request for retrieving draft shipments."""

    URL = "1.0/DraftShipment"


class CreateShipmentRequest(BaseParcelhubApiRequest):
    """Request for creating shipments."""

    URL = "1.0/Shipment"
    METHOD = BaseParcelhubApiRequest.POST

    def params(self, *args, **kwargs):
        """Return request parameters."""
        return {
            "AccountId": self.session.account_id,
            "RequestedLabelFormat": "ZPL",
            "RequestedLabelSize": 6,
        }

    def data(self, *args, **kwargs):
        """Return the request body."""
        shipment_request = kwargs["shipment_request"]
        return etree.tostring(
            shipment_request.as_xml(),
            encoding="utf-8",
            xml_declaration=True,
        )

    def parse_response(self, response, *args, **kwargs):
        """Return the created shipment's shipment ID."""
        ns = "{http://api.parcelhub.net/schemas/api/parcelhub-api-v0.4.xsd}"
        try:
            root = etree.XML(response.text[38:])
            shipment_id = root.find(f"{ns}ParcelhubShipmentId").text
            shipping_info = root.find(f"{ns}ShippingInfo")
            courier_tracking_number = shipping_info.find(
                f"{ns}CourierTrackingNumber"
            ).text
            parcelhub_tracking_number = shipping_info.find(
                f"{ns}ParcelhubTrackingNumber"
            ).text
        except Exception:
            raise exceptions.ResponseParsingError(response.text)
        return CreateShipmentResponse(
            shipment_id=shipment_id,
            courier_tracking_number=courier_tracking_number,
            parcelhub_tracking_number=parcelhub_tracking_number,
        )


class CreateDraftShipmentRequest(CreateShipmentRequest):
    """Request for creating draft shipments."""

    URL = "1.0/DraftShipment"

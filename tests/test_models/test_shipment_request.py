import datetime as dt
from pathlib import Path
from unittest import mock

import pytest
from lxml import etree

from parcelhubapi.models import ShipmentRequest
from parcelhubapi.session import ParcelhubAPISession


@pytest.fixture
def example_request():
    with open(Path(__file__).parent / "shipment_request.xml") as f:
        return f.read()


@pytest.fixture
def mock_session():
    return mock.Mock(account_id="ACCOUNT_ID", NSMAP=ParcelhubAPISession.NSMAP)


@pytest.fixture
def reference():
    return "TEST"


@pytest.fixture
def description():
    return "Goods"


def test_shipment_request(example_request, mock_session, reference, description):
    request = ShipmentRequest(
        session=mock_session,
        reference=reference,
        description=description,
        currency="GBP",
    )
    request.set_service_info(service_id="38001", customer_id="50481", provider_id="50")
    request.set_collection_details(
        collection_date=dt.datetime(2024, 3, 29),
        ready_time=dt.time(12, 0, 0),
        close_time=dt.time(17, 0, 0),
    )
    request.set_collection_address(
        contact_name="TEST001",
        company_name="Parcelhub",
        phone="1",
        address_1="unit a",
        address_2="little tennis street",
        city="nottingham",
        area="NOTTINGHAMSHIRE",
        postcode="ng2 4eu",
        country="GB",
        address_type="Residential",
        email="test@test.test",
    )
    request.set_delivery_address(
        contact_name="TEST",
        company_name="TEST",
        phone="0000000000",
        address_1="TEST",
        address_2=None,
        city="BEVERLY HILLS",
        area="CALIFORNIA",
        postcode="90210",
        country="US",
        address_type="Residential",
        email="test@test.test",
    )
    request.set_customs_declaration(
        terms="DutiesAndTaxesUnpaid",
        postal_charges="0",
        category="Sold",
        category_explanation="ASDAASD",
        value=10,
        insurance_value=10,
        other_value=10,
    )
    package = request.add_package(
        package_type=ShipmentRequest.PARCEL,
        length=20,
        width=20,
        height=20,
        weight=2,
        value="10",
        contents="Goods",
    )
    package.add_item(
        sku="55198",
        description="ASDASDAS",
        product_type="ASDASD",
        value=10,
        quantity=1,
        weight=2,
        country_of_origin="GB",
        hr_code="8498409",
    )
    request_text = etree.tostring(
        request.as_xml(), encoding="utf-8", xml_declaration=True, pretty_print=True
    ).decode("utf8")
    assert request_text == example_request

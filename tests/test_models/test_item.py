import pytest
from lxml import etree

from parcelhubapi.models import ShipmentRequest


@pytest.fixture
def sku():
    return "AAA-BBB-CCC"


@pytest.fixture
def description():
    return "A Product"


@pytest.fixture
def product_type():
    return "Shoes"


@pytest.fixture
def value():
    return "5.25"


@pytest.fixture
def quantity():
    return 2


@pytest.fixture
def weight():
    return 12


@pytest.fixture
def country_of_origin():
    return "CN"


@pytest.fixture
def hr_code():
    return "0994837834983"


@pytest.fixture
def item(
    sku,
    description,
    product_type,
    value,
    quantity,
    weight,
    country_of_origin,
    hr_code,
):
    return ShipmentRequest.Package._Item(
        sku=sku,
        product_type=product_type,
        description=description,
        value=value,
        quantity=quantity,
        weight=weight,
        country_of_origin=country_of_origin,
        hr_code=hr_code,
    )


def test_item_instantiation(
    sku,
    description,
    product_type,
    value,
    quantity,
    weight,
    country_of_origin,
    hr_code,
    item,
):
    assert item.sku == str(sku)
    assert item.description == str(description)
    assert item.product_type == str(product_type)
    assert item.value == str(value)
    assert item.quantity == str(quantity)
    assert item.weight == str(weight)
    assert item.country_of_origin == str(country_of_origin)
    assert item.hr_code == str(hr_code)


def test_to_dict_method(item):
    assert item.to_dict() == {
        item.SKU: item.sku,
        item.DESCRIPTION: item.description,
        item.PRODUCT_TYPE: item.product_type,
        item.VALUE: item.value,
        item.QUANTITY: item.quantity,
        item.WEIGHT: item.weight,
        item.COUNTRY_OF_ORIGIN: item.country_of_origin,
        item.HR_CODE: item.hr_code,
    }


def test_as_xml_method(item):
    expected = (
        "<ItemLevelDeclaration>"
        f"<ProductSKU>{item.sku}</ProductSKU>"
        f"<ProductDescription>{item.description}</ProductDescription>"
        f"<ProductType>{item.product_type}</ProductType>"
        f"<ProductValue>{item.value}</ProductValue>"
        f"<ProductQuantity>{item.quantity}</ProductQuantity>"
        f"<ProductWeight>{item.weight}</ProductWeight>"
        f"<ProductCountryOfOrigin>{item.country_of_origin}</ProductCountryOfOrigin>"
        f"<ProductHarmonisedCode>{item.hr_code}</ProductHarmonisedCode>"
        "</ItemLevelDeclaration>"
    )
    assert etree.tostring(item.as_xml()) == expected.encode("utf8")

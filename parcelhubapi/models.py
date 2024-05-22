"""Models for the parcelhubapi package."""

from lxml import etree


class BaseXMLModel:
    """Base class for creating XML objects."""

    @staticmethod
    def dict_as_xml(root, data):
        """Return a dict as etree.Element."""
        root = etree.Element(root)
        for key, value in data.items():
            etree.SubElement(root, key).text = value
        return root

    def as_xml(self):
        """Return the object's data as etree.Element."""
        return self.dict_as_xml(self.ROOT, self.to_dict())


class ShipmentRequest:
    """Class for creating create shipment requests."""

    ACCOUNT = "Account"
    SHIPMENT_ID = "ParcelhubShipmentId"
    REFERENCE = "Reference1"
    DESCRIPTION = "ContentsDescription"
    PACKAGES = "Packages"
    ENHANCEMENTS = "Enhancements"
    MODIFIED_TIME = "ModifiedTime"
    CURRENCY_CODE = "CurrencyCode"
    DELETED = "Deleted"
    MANIFESTED = "HasBeenManifested"
    TAGS = "ShipmentTags"
    DEPARTMENT = "Department"

    RESIDENTIAL = "Residential"
    BUSINESS = "Business"
    PARCELSHOP = "Parcelshop"

    PARCEL = "Parcel"
    LETTER = "Letter"
    PALLET = "Pallet"

    PAID = "DutiesAndTaxesPaid"
    UNAPID = "DutiesAndTaxesUnpaid"

    def __init__(self, session, reference, description, currency):
        """
        Create a create shipment request.

        Args:
            session (parcelhubapi.session.ParcelhubAPISession): The active session object.
            reference (str): The reference ID of the shipment.
            description (str): A description of the shipment.
            curency (str): The code of the currency the shipment is valued in.
        """
        self.session = session
        self.reference = reference
        self.description = description
        self.currency = currency

        self.service_info = None
        self.collection_details = None
        self.collection_address = None
        self.delivery_address = None
        self.packages = []
        self.customs_declaration = None

    def as_xml(self):
        """Return the request data as xml.etree.Element."""
        root = etree.Element("Shipment", nsmap=self.session.NSMAP)
        etree.SubElement(root, self.ACCOUNT).text = self.session.account_id
        root.append(self.service_info.as_xml())
        etree.SubElement(root, self.SHIPMENT_ID).text = "0"
        root.append(self.collection_details.as_xml())
        root.append(self.collection_address.as_xml())
        root.append(self.delivery_address.as_xml())
        etree.SubElement(root, self.REFERENCE).text = self.reference
        etree.SubElement(root, self.DESCRIPTION).text = self.description
        packages = etree.SubElement(root, self.PACKAGES)
        for package in self.packages:
            packages.append(package.as_xml())
        etree.SubElement(root, self.ENHANCEMENTS)
        etree.SubElement(root, self.MODIFIED_TIME).text = "0001-01-01T00:00:00"
        etree.SubElement(root, self.CURRENCY_CODE).text = self.currency
        root.append(self.customs_declaration.as_xml())
        etree.SubElement(root, self.DELETED).text = "false"
        etree.SubElement(root, self.MANIFESTED).text = "false"
        etree.SubElement(root, self.TAGS)
        etree.SubElement(root, self.DEPARTMENT).text = ""
        return root

    def set_service_info(self, service_id, customer_id, provider_id):
        """
        Set the courier service to be used.

        Args:
            service_id (str): The ID of the service type.
            customer_id (str): The ID of the customer for this service.
            provider_id (str): The ID of the service provider.
        """
        self.service_info = self._ServiceInfo(
            service_id=service_id, customer_id=customer_id, provider_id=provider_id
        )
        return self.service_info

    def set_collection_details(self, collection_date, ready_time, close_time):
        """
        Set details of the shipment collection.

        Args:
            collection_date (datetime.datetime): The date of collection.
            ready_time (datetime.time): The time at which the shipment will be ready.
            close_time (datetime.time): The time at which the collection location closes.
        """
        self.collection_details = self._CollectionDetails(
            collection_date=collection_date,
            ready_time=ready_time,
            close_time=close_time,
        )

    def set_collection_address(
        self,
        contact_name,
        country,
        address_type,
        address_1,
        address_2=None,
        company_name=None,
        phone=None,
        city=None,
        area=None,
        postcode=None,
        email=None,
    ):
        """
        Set the address from which the shipment will be collected.

        Kwargs:
            contact_name (str): The name of the person from which the shipment will be
                collected.
            country (str): The two character identifer of the collection country.
            address_type (str): The type of address. Must be one of
                (ShippingRequest.RESIDENTIAL, ShippingRequest.BUSINESS,
                ShippingRequest.PARCELSHOP)
            address_1 (str): The first line of the collection address.
            address_2 (str): The second line of the collection address.
            company_name (str): The name of the company to be collected from.
            phone (str): Sender contact phone number.
            city (str): The collection city.
            area (str)(optinal): The collection area (county or state).
            postcode (str): The collection postcode.
            email (str): Sender contact email addres.
        """
        self.collection_address = self._CollectionAddress(
            contact_name=contact_name,
            company_name=company_name,
            phone=phone,
            address_1=address_1,
            address_2=address_2,
            city=city,
            area=area,
            postcode=postcode,
            country=country,
            address_type=address_type,
            email=email,
        )
        return self.collection_address

    def set_delivery_address(
        self,
        contact_name,
        country,
        address_type,
        address_1,
        address_2=None,
        company_name=None,
        phone=None,
        city=None,
        area=None,
        postcode=None,
        email=None,
    ):
        """
        Set the address to which the shipment will be delivered.

        Kwargs:
            contact_name (str): The name of the person to which the shipment will be
                delivered.
            country (str): The two character identifer of the delivery country.
            address_type (str): The type of address. Must be one of
                (ShippingRequest.RESIDENTIAL, ShippingRequest.BUSINESS,
                ShippingRequest.PARCELSHOP)
            address_1 (str): The first line of the delivery address.
            address_2 (str): The second line of the delivery address.
            company_name (str): The name of the company to be delivered to.
            phone (str): Recipient contact phone number.
            city (str): The delivery city.
            area (str)(optinal): The delivery area (county or state).
            postcode (str): The delivery postcode.
            email (str): Recipient contact email address.
        """
        self.delivery_address = self._DeliveryAddress(
            contact_name=contact_name,
            company_name=company_name,
            phone=phone,
            address_1=address_1,
            address_2=address_2,
            city=city,
            area=area,
            postcode=postcode,
            country=country,
            address_type=address_type,
            email=email,
        )
        return self.collection_address

    def set_customs_declaration(
        self,
        terms,
        postal_charges=None,
        category=None,
        category_explanation=None,
        value=None,
        insurance_value=None,
        other_value=None,
    ):
        """
        Set the shipment's customs declaration.

        Args:
            terms (str): The terms of trade. Must be one of
                (ShipmentRequest.PAID, ShipmentRequest.UNAPID).

        Kwargs:
            postal_charges (str): The charges for postage.
            category (str): The category of the item.
            category_explanation (str): Explanation of the item category.
            value (str): The shipping value of the shipment.
            insurance_value (str): The insurance value of the shipment.
            other_value (str): Other value of the shipment.

        """
        self.customs_declaration = self._CustomsDeclaration(
            terms=terms,
            postal_charges=postal_charges,
            category=category,
            category_explanation=category_explanation,
            value=value,
            insurance_value=insurance_value,
            other_value=other_value,
        )
        return self.customs_declaration

    def add_package(
        self,
        contents,
        package_type=None,
        length=None,
        width=None,
        height=None,
        weight=None,
        value=None,
    ):
        """
        Add a package to the order.

        Args:
            contents (str): Description of the package contents.

        Kwargs:
            package_type (str): The type of package. Must be one of
                (ShipmentRequest.PARCEL, ShipmentRequest.LETTER, ShipmentRequest.PALLET).
            length (int): The length of the package in cm.
            width (int): The width of the package in cm.
            height (int): The height of the package in cm.
            weight (int): The weight of the package in kg.
            value (str): The sum of the values of the items in the package.

        Returns: parcelhubapi.models.ShipmentRequest.Package.
        """
        package = self.Package(
            package_type=package_type,
            length=length,
            width=width,
            height=height,
            weight=weight,
            value=value,
            currency=self.currency,
            contents=contents,
        )
        self.packages.append(package)
        return package

    class _ServiceInfo(BaseXMLModel):
        ROOT = "ServiceInfo"

        SERVICE_ID = "ServiceId"
        CUSTOMER_ID = "ServiceCustomerUID"
        PROVIDER_ID = "ServiceProviderId"

        def __init__(self, service_id, customer_id, provider_id):
            self.service_id = service_id
            self.customer_id = customer_id
            self.provider_id = provider_id

        def to_dict(self):
            return {
                self.SERVICE_ID: self.service_id,
                self.CUSTOMER_ID: self.customer_id,
                self.PROVIDER_ID: self.provider_id,
            }

    class _CollectionDetails(BaseXMLModel):
        ROOT = "CollectionDetails"

        COLLECTION_DATE = "CollectionDate"
        READY_TIME = "CollectionReadyTime"
        CLOSE_TIME = "LocationCloseTime"

        def __init__(self, collection_date, ready_time, close_time):
            self.collection_date = collection_date
            self.ready_time = ready_time
            self.close_time = close_time

        def to_dict(self):
            return {
                self.COLLECTION_DATE: self.collection_date.strftime("%Y-%m-%d"),
                self.READY_TIME: self.ready_time.strftime("%H:%M:%S"),
                self.CLOSE_TIME: self.close_time.strftime("%H:%M:%S"),
            }

    class _BaseAddress(BaseXMLModel):
        CONTACT_NAME = "ContactName"
        COMPANY_NAME = "CompanyName"
        PHONE = "Phone"
        ADDRESS_1 = "Address1"
        ADDRESS_2 = "Address2"
        CITY = "City"
        AREA = "Area"
        POSTCODE = "Postcode"
        COUNTRY = "Country"
        ADDRESS_TYPE = "AddressType"
        EMAIL = "Email"

        def __init__(
            self,
            contact_name,
            company_name,
            phone,
            address_1,
            address_2,
            city,
            area,
            postcode,
            country,
            address_type,
            email,
        ):
            self.contact_name = contact_name
            self.company_name = company_name
            self.phone = phone
            self.address_1 = address_1
            self.address_2 = address_2
            self.city = city
            self.area = area
            self.postcode = postcode
            self.country = country
            self.address_type = address_type
            self.email = email

        def to_dict(self):
            initial_data = {
                self.CONTACT_NAME: self.contact_name,
                self.COMPANY_NAME: self.company_name,
                self.PHONE: self.phone,
                self.ADDRESS_1: self.address_1,
                self.ADDRESS_2: self.address_2,
                self.CITY: self.city,
                self.AREA: self.area,
                self.POSTCODE: self.postcode,
                self.COUNTRY: self.country,
                self.ADDRESS_TYPE: self.address_type,
                self.EMAIL: self.email,
            }
            data = {
                key: value for key, value in initial_data.items() if value is not None
            }
            return data

    class _CollectionAddress(_BaseAddress):
        ROOT = "CollectionAddress"

    class _DeliveryAddress(_BaseAddress):
        ROOT = "DeliveryAddress"

    class Package(BaseXMLModel):
        """Model for shipment packages."""

        ROOT = "Package"

        PACKAGE_TYPE = "PackageType"
        DIMENSIONS = "Dimensions"
        LENGTH = "Length"
        WIDTH = "Width"
        HEIGHT = "Height"
        WEIGHT = "Weight"
        VALUE = "Value"
        CONTENTS = "Contents"
        CUSTOMS_DECLARATION = "PackageCustomsDeclaration"
        ITEM_DECLARATIONS = "ItemLevelDeclarations"

        def __init__(
            self, package_type, length, width, height, weight, value, currency, contents
        ):
            """Create a shipment package."""
            self.package_type = package_type
            self.length = length
            self.width = width
            self.height = height
            self.weight = weight
            self.value = value
            self.currency = currency
            self.contents = contents
            self.items = []

        def add_item(
            self,
            sku=None,
            description=None,
            product_type=None,
            value=None,
            quantity=None,
            weight=None,
            country_of_origin=None,
            hr_code=None,
        ):
            """
            Add an item to the package.

            Args:
                sku (str): The item SKU.
                description (str): A description of the item,
                    e.g. 'blue cotton shirt' .
                product_type (str): The type of item, e.g. 'shirt'.
                value (int): The value of the product.
                quantity (int): The number of the product being sent.
                weight (int): The weight of the item in kg.
                country_of_origin (str): The two character country code of the product's origin.
                hr_code (str): The product's harmonised code.
            """
            item = self._Item(
                sku=sku,
                description=description,
                product_type=product_type,
                value=value,
                quantity=quantity,
                weight=weight,
                country_of_origin=country_of_origin,
                hr_code=hr_code,
            )
            self.items.append(item)
            return item

        def as_xml(self):
            """Return the package data s lxml.etree.Element."""
            root = etree.Element(self.ROOT)
            etree.SubElement(root, self.PACKAGE_TYPE).text = self.package_type
            dimensions = etree.SubElement(root, self.DIMENSIONS)
            etree.SubElement(dimensions, self.LENGTH).text = str(self.length)
            etree.SubElement(dimensions, self.WIDTH).text = str(self.width)
            etree.SubElement(dimensions, self.HEIGHT).text = str(self.height)
            etree.SubElement(root, self.WEIGHT).text = str(self.weight)
            etree.SubElement(root, self.VALUE, Currency=self.currency).text = str(
                self.value
            )
            etree.SubElement(root, self.CONTENTS).text = self.contents
            customs_declaration = etree.SubElement(root, self.CUSTOMS_DECLARATION)
            etree.SubElement(customs_declaration, self.WEIGHT).text = (
                f"{self.weight} kg"
            )
            etree.SubElement(
                customs_declaration, self.VALUE, Currency=self.currency
            ).text = str(self.value)
            items_declaration = etree.SubElement(root, self.ITEM_DECLARATIONS)
            for item in self.items:
                items_declaration.append(item.as_xml())
            return root

        class _Item(BaseXMLModel):
            ROOT = "ItemLevelDeclaration"

            SKU = "ProductSKU"
            DESCRIPTION = "ProductDescription"
            PRODUCT_TYPE = "ProductType"
            VALUE = "ProductValue"
            QUANTITY = "ProductQuantity"
            WEIGHT = "ProductWeight"
            COUNTRY_OF_ORIGIN = "ProductCountryOfOrigin"
            HR_CODE = "ProductHarmonisedCode"

            def __init__(
                self,
                sku,
                description,
                product_type,
                value,
                quantity,
                weight,
                country_of_origin,
                hr_code,
            ):
                self.sku = str(sku)
                self.description = str(description)
                self.product_type = str(product_type)
                self.value = str(value)
                self.quantity = str(quantity)
                self.weight = str(weight)
                self.country_of_origin = str(country_of_origin)
                self.hr_code = str(hr_code)

            def to_dict(self):
                """Return the item as a dict."""
                initial_data = {
                    self.SKU: self.sku,
                    self.DESCRIPTION: self.description,
                    self.PRODUCT_TYPE: self.product_type,
                    self.VALUE: self.value,
                    self.QUANTITY: self.quantity,
                    self.WEIGHT: self.weight,
                    self.COUNTRY_OF_ORIGIN: self.country_of_origin,
                    self.HR_CODE: self.hr_code,
                }
                data = {
                    key: value
                    for key, value in initial_data.items()
                    if value is not None
                }
                return data

    class _CustomsDeclaration(BaseXMLModel):
        ROOT = "CustomsDeclarationInfo"

        TERMS = "TermsOfTrade"
        POSTAL_CHARGES = "PostalCharges"
        CATEGORY = "CategoryOfItem"
        CATEGORY_EXPLANATION = "CategoryOfItemExplanation"
        VALUE = "CarriageValue"
        INSURANCE_VALUE = "InsuranceValue"
        OTHER_VALUE = "OtherValue"

        def __init__(
            self,
            terms,
            postal_charges,
            category,
            category_explanation,
            value,
            insurance_value,
            other_value,
        ):
            self.terms = terms
            self.postal_charges = postal_charges
            self.category = category
            self.category_explanation = category_explanation
            self.value = str(value)
            self.insurance_value = str(insurance_value)
            self.other_value = str(other_value)

        def to_dict(self):
            return {
                self.TERMS: self.terms,
                self.POSTAL_CHARGES: self.postal_charges,
                self.CATEGORY: self.category,
                self.CATEGORY_EXPLANATION: self.category_explanation,
                self.VALUE: self.value,
                self.INSURANCE_VALUE: self.insurance_value,
                self.OTHER_VALUE: self.other_value,
            }

from parcelhubapi.models import CreateShipmentResponse


def test_create_shipment_response():
    shipment_id = "039454035809"
    courier_tracking_number = "4389075048375430"
    parcelhub_tracking_number = "829075483504354"
    obj = CreateShipmentResponse(
        shipment_id=shipment_id,
        courier_tracking_number=courier_tracking_number,
        parcelhub_tracking_number=parcelhub_tracking_number,
    )
    assert obj.shipment_id == shipment_id
    assert obj.courier_tracking_number == courier_tracking_number
    assert obj.parcelhub_tracking_number == parcelhub_tracking_number

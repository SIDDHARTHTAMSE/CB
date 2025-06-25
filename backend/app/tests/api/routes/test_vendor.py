import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Vendor
from app.core.config import settings


# def test_create_new_vendor(client: TestClient, db: Session) -> None:
#     data = {
#         "vendor_code": "V1234",
#         "vendor_name": "Vendor One",
#         "country": "Country X",
#         "state": "State Y",
#         "district": "District Z",
#         "city": "City A",
#         "pincode": "123456",
#         "contact_no": "987654321"
#     }
#     response = client.post("/vendors", json=data)
#     assert response.status_code == 201
#     content = response.json()
#     assert content["vendor_code"] == data["vendor_code"]
#     assert content["vendor_name"] == data["vendor_name"]
#     assert content["country"] == data["country"]
#     assert content["state"] == data["state"]
#     assert content["district"] == data["district"]
#     assert content["city"] == data["city"]
#     assert content["pincode"] == data["pincode"]
#     assert content["contact_no"] == data["contact_no"]

    # db_vendor = db.query(Vendor).filter(Vendor.vendor_code == data["vendor_code"]).first()
    # assert db_vendor is not None
    # assert db_vendor.vendor_name == data["vendor_name"]


def test_for_create_vendor(
        client: TestClient,
        super_token_headers: dict[str, str]
) -> None:
    data = {
        "vendor_code": "V1234",
        "vendor_name": "Vendor One",
        "country": "Country X",
        "state": "State Y",
        "district": "District Z",
        "city": "City A",
        "pincode": "123456",
        "contact_no": "987654321"
    }
    response = client.post(
        f"{settings.API_V1_STR}/vendors",
        headers=super_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["vendor_code"] == data["vendor_code"]
    assert content["vendor_name"] == data["vendor_name"]
    assert content["country"] == data["country"]
    assert content["state"] == data["state"]
    assert content["district"] == data["district"]
    assert content["city"] == data["city"]
    assert content["pincode"] == data["pincode"]
    assert content["contact_no"] == data["contact_no"]
    assert "id" in content

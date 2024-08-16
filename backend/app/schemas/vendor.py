from pydantic import BaseModel

from app.models import Vendor


class CreateVendor(BaseModel):
    vendor_code: str
    vendor_name: str
    country: str
    state: str
    district: str
    city: str
    pincode: str
    contact_no: str


class CreateVendorRes(BaseModel):
    vendor_code: str
    vendor_name: str
    country: str
    state: str
    district: str
    city: str
    pincode: str
    contact_no: str


def to_vendor_res(vendor: Vendor):
    """Convert DB model to response model"""
    return CreateVendorRes(
        vendor_code=vendor.vendor_code,
        vendor_name=vendor.name,
        country=vendor.country,
        state=vendor.state,
        district=vendor.district,
        city=vendor.city,
        pincode=vendor.pin_code,
        contact_no=vendor.contact_number
    ).dict()

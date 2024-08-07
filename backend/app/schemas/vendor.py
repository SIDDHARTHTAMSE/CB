from pydantic import BaseModel

from app.models import Vendor


class CreateVendor(BaseModel):
    vendor_code: str
    vendor_name: str


class CreateVendorRes(BaseModel):
    vendor_code: str
    vendor_name: str


def to_vendor_res(vendor: Vendor):
    """Convert DB model to response model"""
    return CreateVendorRes(
        vendor_code=vendor.vendor_code,
        vendor_name=vendor.name
    ).dict()

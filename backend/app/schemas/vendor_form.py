from pydantic import BaseModel

from app.models import VendorForm


class CreateVendorForm(BaseModel):
    vendor_code: str
    vendor_name: str
    address: str
    contact_no: str


class CreateVendorFormRes(BaseModel):
    vendor_code: str
    vendor_name: str
    address: str
    contact_no: str

from typing import List

from fastapi import APIRouter, HTTPException

from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from uuid import UUID

from app.api.deps import SessionDep
from app.crud import get_vendor_by_code, create_vendor, get_vendors, delete_by_vendor, update_vendor
from app.models import Vendor
from app.schemas import vendor

router = APIRouter()


@router.post("/", response_model=vendor.CreateVendorRes)
def create_new_vendor(session: SessionDep, vendor_req: vendor.CreateVendor):
    existing_vendor = get_vendor_by_code(
        session=session, code=vendor_req.vendor_code
    )

    if existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vendor with same code already exists"
        )
    new_vendor = Vendor()
    new_vendor.vendor_code = vendor_req.vendor_code
    new_vendor.name = vendor_req.vendor_name
    new_vendor.country = vendor_req.country
    new_vendor.state = vendor_req.state
    new_vendor.district = vendor_req.district
    new_vendor.city = vendor_req.city
    new_vendor.pin_code = vendor_req.pincode
    new_vendor.contact_number = vendor_req.contact_no
    new_vendor = create_vendor(session=session, vendor=new_vendor)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=vendor.to_vendor_res(new_vendor)
    )


@router.get("{vendor_code}", response_model=vendor.CreateVendorRes)
def get_vendor(session: SessionDep, vendor_code: str):
    existing_vendor = get_vendor_by_code(session=session, code=vendor_code)

    if not existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor status_code not found"
        )
    return vendor.to_vendor_res(existing_vendor)


@router.get("/", response_model=List[vendor.CreateVendorRes])
def get_vendor_details(session: SessionDep):
    vendors = get_vendors(session=session)
    return [vendor.to_vendor_res(v) for v in vendors]


@router.delete("{vendor_code}")
def delete_vendor(session: SessionDep, vendor_code: str):
    vendor_to_delete = get_vendor_by_code(session=session, code=vendor_code)

    if not vendor_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor code not found"
        )

    delete_by_vendor(session=session, vendor=vendor_to_delete)
    return JSONResponse(
        content="Vendor code successfully deleted"
    )


@router.put("/{vendor_code}", response_model=vendor.CreateVendorRes)
def update_existing_vendor(
        session: SessionDep,
        vendor_code: str,
        vendor_req: vendor.UpdateVendor
):
    # null check
    existing_vendor = get_vendor_by_code(session=session, code=vendor_code)
    if not existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    existing_vendor.name = vendor_req.vendor_name or existing_vendor.name
    existing_vendor.country = vendor_req.country or existing_vendor.country
    existing_vendor.state = vendor_req.state or existing_vendor.state
    existing_vendor.district = vendor_req.district or existing_vendor.district
    existing_vendor.city = vendor_req.city or existing_vendor.city
    existing_vendor.pin_code = vendor_req.pincode or existing_vendor.pin_code
    existing_vendor.contact_number = vendor_req.contact_no or existing_vendor.contact_number

    existing_vendor = update_vendor(session=session, vendor=existing_vendor)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=vendor.to_vendor_res(existing_vendor)
    )

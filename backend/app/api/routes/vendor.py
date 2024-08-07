from fastapi import APIRouter, HTTPException

from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse

from app.api.deps import SessionDep
from app.crud import get_vendor_by_code, create_vendor
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
    new_vendor = create_vendor(session=session, vendor=new_vendor)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=vendor.to_vendor_res(new_vendor)
    )

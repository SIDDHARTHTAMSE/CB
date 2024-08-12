from fastapi import APIRouter, HTTPException
from app.schemas.vendor_form import CreateVendorForm, CreateVendorFormRes
from app.api.deps import SessionDep
from app.models import VendorForm
from app.crud import create_vendor_form
from fastapi.responses import JSONResponse
from fastapi import status


router = APIRouter()


@router.post("/", response_model=CreateVendorFormRes)
def create_by_vendor_form(session: SessionDep, vendor_req: CreateVendorForm):

    vendor_form = VendorForm()
    vendor_form.vendor_name = vendor_req.vendor_name
    vendor_form.vendor_code = vendor_req.vendor_code
    vendor_form.address = vendor_req.address
    vendor_form.contact_no = vendor_req.contact_no

    create_vendor_form(session=session, vendor_form=vendor_form)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Successfully created"
    )

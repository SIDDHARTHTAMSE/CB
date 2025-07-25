from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import get_all_payment_details, get_payment_detail_by_id, get_reference_number, create_payment_details, update_payment_details, delete_payment_details, get_instructor_by_id
from app.models import PaymentDetails
from app.schemas import payment_details
from uuid import UUID

router = APIRouter()


@router.post('/', response_model=payment_details.CreatePaymentMethodRes)
def create_new_payment_details(session: SessionDep, user_req: payment_details.CreatePaymentMethod):
    existing_reference = get_reference_number(
        session=session, ref_no=user_req.reference_number
    )

    if existing_reference:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reference number is already exists"
        )

    existing_instructor = get_instructor_by_id(
        session=session,
        instructor_id=user_req.instructor_id
    )

    if not existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor id is not found"
        )

    new_payment_details = PaymentDetails()
    new_payment_details.instructor_id = user_req.instructor_id
    new_payment_details.status = user_req.status
    new_payment_details.reference_number = user_req.reference_number
    new_payment_details.payment_date = user_req.payment_date
    new_payment_details.payment_method = user_req.payment_method
    new_payment_details.amount = user_req.amount
    new_payment_details.currency = user_req.currency

    new_payment_details = create_payment_details(session=session, payment_details=new_payment_details)
    return payment_details.to_payment_detail_res(new_payment_details)


@router.get('/', response_model=List[payment_details.CreatePaymentMethodRes])
def get_all_payment_detail(session: SessionDep):
    get_payment_details = get_all_payment_details(session=session)
    return [payment_details.to_payment_detail_res(s) for s in get_payment_details]

from typing import Optional
from pydantic import BaseModel
from app.models import PaymentDetails
from uuid import UUID
from datetime import date


class CreatePaymentMethod(BaseModel):
    instructor_id: UUID
    status: str
    amount: str
    payment_date: date
    payment_method: str
    reference_number: str
    currency: str


class CreatePaymentMethodRes(CreatePaymentMethod):
    pass


class UpdatePaymentMethod(BaseModel):
    instructor_id: Optional[UUID] = None
    status: Optional[str] = None
    amount: Optional[str] = None
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None
    reference_number: Optional[str] = None
    currency: Optional[str] = None


def to_payment_detail_res(payment_detail: PaymentDetails):
    return CreatePaymentMethodRes(
        instructor_id=payment_detail.instructor_id,
        status=payment_detail.status,
        amount=payment_detail.amount,
        payment_date=payment_detail.payment_date,
        payment_method=payment_detail.payment_method,
        reference_number=payment_detail.reference_number,
        currency=payment_detail.currency
    )

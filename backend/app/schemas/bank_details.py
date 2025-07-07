from pydantic import BaseModel, Field, constr
from uuid import UUID
from typing import Optional
from app.models import BankDetails


class CreateBankDetails(BaseModel):
    register_id: UUID
    bank_name: str = Field(..., example="HDFC BANK")
    account_holder_name: str = Field(..., example="Siddharth Tamse")
    upi_id: constr(pattern=r'^[\w.-]+@[\w.-]+$') = Field(..., example="john.doe@okaxis")
    account_no: constr(min_length=9, max_length=10) = Field(..., example="1234567890")
    ifsc_code: constr(pattern=r'^[A-Z]{4}0[A-Z0-9]{6}$') = Field(..., example="HDFC0001234")


class CreateBankDetailsRes(CreateBankDetails):
    pass


class UpdateDetails(BaseModel):
    register_id: Optional[UUID] = None
    bank_name: Optional[str] = Field(default=None, example="HDFC BANK")
    account_holder_name: Optional[str] = Field(default=None, example="Siddharth Tamse")
    upi_id: Optional[constr(pattern=r'^[\w.-]+@[\w.-]+$')] = Field(default=None, example="john.doe@okaxis")
    ifsc_code: Optional[constr(pattern=r'^[A-Z]{4}0[A-Z0-9]{6}$')] = Field(default=None, example="HDFC0001234")


def to_bank_details_res(bankdetails: BankDetails):
    return CreateBankDetailsRes(
        register_id=bankdetails.register_id,
        bank_name=bankdetails.bank_name,
        account_holder_name=bankdetails.account_holder_name,
        upi_id=bankdetails.upi_id,
        account_no=bankdetails.account_no,
        ifsc_code=bankdetails.ifsc_code
    )

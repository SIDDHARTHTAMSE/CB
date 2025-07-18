from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import (
    get_all_bankdetails,
    get_bank_user_by_account,
    create_bank_user,
    delete_bank_user,
    update_bank_user,
    get_register_id,
    get_upi,
    get_ifsc_code
)
from app.models import BankDetails
from app.schemas import bank_details

router = APIRouter()


@router.post("/", response_model=bank_details.CreateBankDetailsRes)
def create_new_bank_user(session: SessionDep, user_req: bank_details.CreateBankDetails):
    existing_user = get_bank_user_by_account(
        session=session,
        account_no=user_req.account_no
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with account number already exist"
        )

    existing_upi = get_upi(session=session, upi=user_req.upi_id)
    if existing_upi:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with UPI id is already exist"
        )

    existing_ifsc = get_ifsc_code(session=session, ifsc=user_req.ifsc_code)
    if existing_ifsc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with IFSC code is already exist"
        )

    existing_register = get_register_id(session=session, register_id=user_req.register_id)
    if not existing_register:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with register is not found"
        )

    new_user = BankDetails()
    new_user.register_id = user_req.register_id
    new_user.bank_name = user_req.bank_name
    new_user.account_no = user_req.account_no
    new_user.upi_id = user_req.upi_id
    new_user.ifsc_code = user_req.ifsc_code
    new_user.account_holder_name = user_req.account_holder_name

    new_user = create_bank_user(
        session=session, bank_user=new_user
    )
    return bank_details.to_bank_details_res(new_user)


@router.get("/", response_model=List[bank_details.CreateBankDetailsRes])
def get_all_bank_users(session: SessionDep):
    get_bank_users = get_all_bankdetails(session=session)
    return [bank_details.to_bank_details_res(s) for s in get_bank_users]


@router.get("{account_no}", response_model=bank_details.CreateBankDetailsRes)
def get_bank_user_by_account_no(session: SessionDep, account_no: str):
    existing_account = get_bank_user_by_account(
        session=session,
        account_no=account_no
    )

    if not existing_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with account number not found"
        )
    return bank_details.to_bank_details_res(existing_account)


@router.put("{account_no}", response_model=bank_details.CreateBankDetailsRes)
def update_bank_user_by_account_no(
        session: SessionDep,
        account_no: str,
        user_req: bank_details.UpdateBankDetails
):
    existing_account = get_bank_user_by_account(session=session, account_no=account_no)
    if not existing_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with account number not found"
        )

    existing_account.register_id = user_req.register_id or existing_account.register_id
    existing_account.bank_name = user_req.bank_name or existing_account.bank_name
    existing_account.account_holder_name = user_req.account_holder_name or existing_account.account_holder_name
    existing_account.upi_id = user_req.upi_id or existing_account.upi_id
    existing_account.ifsc_code = user_req.ifsc_code or existing_account.ifsc_code

    update_user = update_bank_user(session=session, bank_user=existing_account)
    return bank_details.to_bank_details_res(update_user)


@router.delete("{account_no}", response_model=bank_details.CreateBankDetailsRes)
def delete_bank_user_by_account_no(session: SessionDep, account_no: str):
    existing_bank_user = get_bank_user_by_account(session=session, account_no=account_no)
    if not existing_bank_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with account number is not found"
        )
    delete_bank_user(session=session, bank_user=existing_bank_user)
    return JSONResponse(
        content="User deleted successfully"
    )

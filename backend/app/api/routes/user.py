from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import get_all_users, get_users_by_email,get_users_by_phone, create_users, update_users, delete_users
from app.models import Register
from app.schemas import user

router = APIRouter()


@router.post("/", response_model=user.CreateUsersRes)
def create_new_users(session: SessionDep, user_req: user.CreateUsers):
    existing_users = get_users_by_email(
        session=session, email=user_req.email
    )

    if existing_users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Users with same email is already exists"
        )

    existing_users = get_users_by_phone(
        session=session, number=user_req.phone_number
    )

    if existing_users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Users with phone number is already exists"
        )
    new_users = Register()
    new_users.first_name = user_req.first_name
    new_users.last_name = user_req.last_name
    new_users.email = user_req.email
    new_users.password = user_req.password
    new_users.phone_number = user_req.phone_number
    new_users.gender = user_req.gender
    new_users.date_of_birth = user_req.date_of_birth

    new_users = create_users(session=session, users=new_users)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=user.to_users_res(new_users)
    )


@router.get("/", response_model=List[user.CreateUsersRes])
def get_users_details(session: SessionDep):
    users = get_all_users(session=session)
    return [user.to_users_res(s) for s in users]

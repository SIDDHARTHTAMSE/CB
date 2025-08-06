from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import get_all_user_device, get_user_device_using_id,  delete_user_device, create_user_device, update_user_device, get_register_id
from app.models import UserDevice
from app.schemas import user_device
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=user_device.CreateUserDeviceRes)
def create_new_user_device(session: SessionDep, user_req: user_device.CreateUserDevice):
    existing_register = get_register_id(
        session=session,
        register_id=user_req.register_id
    )

    if not existing_register:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Register id is not found"
        )

    new_user_device = UserDevice()
    new_user_device.register_id = user_req.register_id
    new_user_device.device_info = user_req.device_info
    new_user_device.last_used = user_req.last_used
    new_user_device.is_active = user_req.is_active
    new_user_device.location = user_req.location

    new_user_device = create_user_device(
        session=session, user_device=new_user_device
    )
    return user_device.to_user_device_res(new_user_device)


@router.get("/", response_model=List[user_device.CreateUserDeviceRes])
def get_all_new_user_device(session: SessionDep):
    get_user_device = get_all_user_device(session=session)
    return [user_device.to_user_device_res(s) for s in get_user_device]


@router.get("{user_device_no}", response_model=user_device.CreateUserDeviceRes)
def get_user_device_using_user_device(session: SessionDep, user_device_no: UUID):
    existing_user_id = get_user_device_using_id(session=session, user_id=user_device_no)
    if not existing_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User device is not found"
        )
    return user_device.to_user_device_res(existing_user_id)

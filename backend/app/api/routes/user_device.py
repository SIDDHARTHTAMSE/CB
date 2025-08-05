from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import get_all_user_device, get_user_device_using_id,  delete_user_device, create_user_device, update_user_device, get_register_id
from app.models import UserDevice
from app.schemas import user_device

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

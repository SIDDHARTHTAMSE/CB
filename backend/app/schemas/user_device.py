from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from app.models import UserDevice
from datetime import date


class CreateUserDevice(BaseModel):
    register_id: UUID
    device_info: str
    last_used: date
    is_active: bool = False
    location: str


class CreateUserDeviceRes(CreateUserDevice):
    pass


class UpdateUserDevice(BaseModel):
    register_id: Optional[UUID] = None
    device_info: Optional[str] = None
    last_used: Optional[date] = None
    is_active: Optional[bool] = None
    location: Optional[str] = None


def to_user_device_res(user_device: UserDevice):
    return CreateUserDeviceRes(
        register_id=user_device.register_id,
        device_info=user_device.device_info,
        last_used=user_device.last_used,
        is_active=user_device.is_active,
        location=user_device.location
    ).dict()

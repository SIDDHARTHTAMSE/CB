from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.models import UserLoginLogs
from datetime import date


class CreateUserLoginLogs(BaseModel):
    register_id: UUID
    log_id: str
    login_time: date
    logout_time: date
    location: str
    device: str


class UserLogsLoginRes(CreateUserLoginLogs):
    pass


class UpdateUserLoginLogs(BaseModel):
    register_id: Optional[UUID] = None
    log_id: Optional[str] = None
    login_time: Optional[date] = None
    logout_time: Optional[date] = None
    location: Optional[str] = None
    device: Optional[str] = None


def to_user_login_logs_res(user_logs: UserLoginLogs):
    return UserLogsLoginRes(
        register_id=user_logs.register_id,
        log_id=user_logs.log_id,
        login_time=user_logs.login_time,
        logout_time=user_logs.logout_time,
        location=user_logs.location,
        device=user_logs.device
    )

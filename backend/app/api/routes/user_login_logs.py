from app.models import UserLoginLogs, Register
from app.schemas import user_login_logs
from app.api.deps import SessionDep, HTTPException, status
from fastapi import APIRouter
from typing import List
from app.crud import (get_user_login_logs,
                      create_user_login_logs,
                      delete_user_login_logs,
                      update_user_login_logs,
                      get_user_login_logs_by_id,
                      get_user_login_logs_by_login_id,
                      get_register_id
                      )

router = APIRouter()


@router.post("/", response_model=user_login_logs.UserLogsLoginRes)
def create_new_user_login_logs(session: SessionDep, user_req: user_login_logs.CreateUserLoginLogs):
    existing_login_id = get_user_login_logs_by_login_id(session=session, login_id=user_req.log_id)
    if existing_login_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Login id is already exists"
        )

    existing_register_id = get_register_id(session=session, register_id=user_req.register_id)
    if not existing_register_id:
        raise  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Register id is not found"
        )

    new_login_logs = UserLoginLogs()
    new_login_logs.register_id = user_req.register_id
    new_login_logs.log_id = user_req.log_id
    new_login_logs.login_time = user_req.login_time
    new_login_logs.logout_time = user_req.logout_time
    new_login_logs.device = user_req.device
    new_login_logs.location = user_req.location

    new_login_logs = create_user_login_logs(session=session, login_logs=new_login_logs)
    return user_login_logs.to_user_login_logs_res(new_login_logs)


@router.get("/", response_model=List[user_login_logs.UserLogsLoginRes])
def get_all_user_login_logs(session: SessionDep):
    get_all_new_users_login_logs = get_user_login_logs(session=session)
    return [user_login_logs.to_user_login_logs_res(s) for s in get_all_new_users_login_logs]

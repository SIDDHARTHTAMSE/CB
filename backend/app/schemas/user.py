from typing import Optional
from pydantic import BaseModel
from app.models import Register


class CreateUsers(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    date_of_birth: str
    gender: str


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None


class CreateUsersRes(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    date_of_birth: str
    gender: str


def to_users_res(users: Register):
    return CreateUsersRes(
        first_name=users.first_name,
        last_name=users.last_name,
        email=users.email,
        password=users.password,
        phone_number=users.phone_number,
        date_of_birth=users.date_of_birth,
        gender=users.gender
    ).dict()

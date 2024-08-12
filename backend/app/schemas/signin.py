from pydantic import BaseModel

from app.models import SignIn


class CreateSignin(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


class CreateSigninRes(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


def to_signin_res(signin: SignIn):
    return CreateSigninRes(
        name=signin.name,
        email=signin.email,
        password=signin.password,
        confirm_password=signin.confirm_password
    ).dict()

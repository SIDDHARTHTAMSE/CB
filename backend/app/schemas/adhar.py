from pydantic import BaseModel

from app.models import AdharCard
from typing import Optional


class CreateAdhar(BaseModel):
    adhar_no: str
    first_name: str
    last_name: str
    gender: str


class UpdateAdhar(BaseModel):
    first_name: str
    last_name: str
    gender: str


class CreateAdharRes(BaseModel):
    adhar_no: str
    first_name: str
    last_name: str
    gender: str


def is_adhar_res(adhar: AdharCard):
    return CreateAdharRes(
        adhar_no=adhar.adhar_no,
        first_name=adhar.first_name,
        last_name=adhar.last_name,
        gender=adhar.gender
    ).dict()


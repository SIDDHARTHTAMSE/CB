from typing import Optional
from pydantic import BaseModel
from app.models import Qualification
from uuid import UUID
from datetime import date


class CreateQualification(BaseModel):
    instructor_id: UUID
    degree_type: str
    specialization: str
    time_period: date
    verification_status: str
    verified_on: date


class CreateQualificationRes(CreateQualification):
    pass


class UpdateQualification(BaseModel):
    instructor_id: Optional[UUID] = None
    degree_type: Optional[str] = None
    specialization: Optional[str] = None
    time_period: Optional[date] = None
    verification_status: Optional[str] = None
    verified_on: Optional[date] = None


def to_qualification_res(qualification: Qualification):
    return CreateQualificationRes(
        instructor_id=qualification.instructor_id,
        degree_type=qualification.degree_type,
        specialization=qualification.specialization,
        time_period=qualification.time_period,
        verification_status=qualification.verification_status,
        verified_on=qualification.verified_on
    )

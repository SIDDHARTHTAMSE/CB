from typing import Optional
from pydantic import BaseModel
from app.models import Experience
from uuid import UUID
from datetime import date


class CreateExperience(BaseModel):
    instructor_id: UUID
    position: str
    company_name: str
    time_period: date
    description: str
    verification_status: str
    remarks: str
    verified_on: date


class CreateExperienceRes(CreateExperience):
    pass


class UpdateExperience(BaseModel):
    instructor_id: Optional[UUID] = None
    position: Optional[str] = None
    company_name: Optional[str] = None
    time_period: Optional[date] = None
    description: Optional[str] = None
    verification_status: Optional[str] = None
    remarks: Optional[str] = None
    verified_on: Optional[date] = None


def to_experience_res(experience: Experience):
    return CreateExperienceRes(
        instructor_id=experience.instructor_id,
        position=experience.position,
        company_name=experience.company_name,
        time_period=experience.time_period,
        description=experience.description,
        verification_status=experience.verification_status,
        remarks=experience.remarks,
        verified_on=experience.verified_on
    )

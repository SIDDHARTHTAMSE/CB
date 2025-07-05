from typing import Optional
from pydantic import BaseModel
from app.models import Instructor
from uuid import UUID
from datetime import date


class CreateInstructor(BaseModel):
    register_id: UUID
    language: str
    bio: str
    verification_status: str
    verification_id: str
    remarks: str
    verify_on: date


class CreateInstructorResponse(CreateInstructor):
    pass


class UpdateInstructor(BaseModel):
    language: Optional[str] = None
    bio: Optional[str] = None
    verification_status: Optional[str] = None
    verification_id: Optional[str] = None
    remarks: Optional[str] = None
    verify_on: Optional[date] = None


def to_instructor_res(instructor: Instructor):
    return CreateInstructorResponse(
        register_id=instructor.register_id,
        language=instructor.language,
        bio=instructor.bio,
        verification_status=instructor.verification_status,
        verification_id=instructor.verification_id,
        remarks=instructor.remarks,
        verify_on=instructor.verify_on
    )


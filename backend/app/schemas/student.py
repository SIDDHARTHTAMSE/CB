from pydantic import BaseModel

from app.models import Students
from typing import Optional


class CreateStudent(BaseModel):
    student_first_name: str
    student_last_name: str
    student_usn: str


class UpdateStudent(BaseModel):
    student_first_name: Optional[str] = None
    student_last_name: Optional[str] = None


class CreateStudentRes(BaseModel):
    student_first_name: str
    student_last_name: str
    student_usn: str


def is_stud_res(student: Students):
    return CreateStudentRes(
        student_first_name=student.student_first_name,
        student_last_name=student.student_last_name,
        student_usn=student.student_usn
    ).dict()


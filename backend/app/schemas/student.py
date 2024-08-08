from pydantic import BaseModel

from app.models import Students


class CreateStudent(BaseModel):
    student_first_name: str
    student_last_name: str
    student_usn: str


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


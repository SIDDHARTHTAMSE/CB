from typing import List

from fastapi import APIRouter, HTTPException, status
from app.schemas.student import CreateStudent, CreateStudentRes
from app.api.deps import SessionDep
from app.crud import get_student_by_usn, create_student, get_student, delete_student, update_student
from app.schemas.student import is_stud_res
from fastapi.responses import JSONResponse
from app.models import Students
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=CreateStudentRes)
def create_new_student(session: SessionDep, student_req: CreateStudent):
    existing_student = get_student_by_usn(
        session=session, usn=student_req.student_usn
    )

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student USN is already exist"
        )

    stud = Students()
    stud.student_first_name = student_req.student_first_name
    stud.student_last_name = student_req.student_last_name
    stud.student_usn = student_req.student_usn
    stud = create_student(session=session, student=stud)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=is_stud_res(stud)
    )


@router.get("/", response_model=List[CreateStudentRes])
def get_student_details(session: SessionDep):
    students = get_student(session=session)
    return [is_stud_res(s) for s in students]


@router.get("{student_usn}", response_model=CreateStudentRes)
def get_usn_by_student(session: SessionDep, student_usn: str):
    existing_usn = get_student_by_usn(session=session, usn=student_usn)

    if not existing_usn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student usn not found"
        )
    return is_stud_res(existing_usn)


@router.delete("{student_usn}")
def delete_by_student_usn(session: SessionDep, student_usn: str):
    existing_usn = get_student_by_usn(session=session, usn=student_usn)

    if not existing_usn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student us is not found"
        )
    delete_student(session=session, student=existing_usn)
    return JSONResponse(
        content="Student usn deleted successfully"
    )


@router.put("{student_id}", response_model=CreateStudentRes)
def update_by_student(session: SessionDep, student_id: UUID, student_req: CreateStudent):
    existing_student = update_student(
        session=session,
        student_id=student_id,
        student_first_name=student_req.student_first_name,
        student_last_name=student_req.student_last_name,
        student_usn=student_req.student_usn
    )

    if existing_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Updated successfully"
    )
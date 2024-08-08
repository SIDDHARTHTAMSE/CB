from fastapi import APIRouter, HTTPException, status
from app.schemas.student import CreateStudent, CreateStudentRes
from app.api.deps import SessionDep
from app.crud import get_student_by_usn, create_student
from app.schemas.student import is_stud_res
from fastapi.responses import JSONResponse
from app.models import Students

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
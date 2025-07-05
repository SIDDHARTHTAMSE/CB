from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import get_all_instructor, get_instructor_by_user_id, create_instructor, update_instructor, delete_instructor
from app.models import Instructor
from app.schemas import instructor

router = APIRouter()


@router.post("/", response_model=instructor.CreateInstructorResponse)
def create_new_instructor(session: SessionDep, instructor_req: instructor.CreateInstructor):
    existing_instructor = get_instructor_by_user_id(
        session=session,
        user_id=instructor_req.register_id
    )

    if existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Instructor with register id is already exist"
        )

    new_instructor = Instructor()
    new_instructor.register_id = instructor_req.register_id
    new_instructor.language = instructor_req.language
    new_instructor.bio = instructor_req.bio
    new_instructor.verification_status = instructor_req.verification_status
    new_instructor.verification_id = instructor_req.verification_id
    new_instructor.remarks = instructor_req.remarks
    new_instructor.verify_on = instructor_req.verify_on

    new_instructor = create_instructor(session=session, instructor=new_instructor)
    return instructor.to_instructor_res(new_instructor)


@router.get("/", response_model=List[instructor.CreateInstructorResponse])
def get_all_instructors(session: SessionDep):
    instructors = get_all_instructor(session=session)
    return [instructor.to_instructor_res(s) for s in instructors]

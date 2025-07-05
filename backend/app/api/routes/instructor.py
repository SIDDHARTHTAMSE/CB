from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import get_all_instructor, get_instructor_by_user_id, create_instructor, update_instructor, delete_instructor, get_instructor_by_id
from app.models import Instructor
from app.schemas import instructor
from uuid import UUID

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


@router.get("{register_id}", response_model=instructor.CreateInstructorResponse)
def get_instructors_by_register_id(session: SessionDep, register_id: UUID):
    existing_instructors = get_instructor_by_user_id(session=session, user_id=register_id)

    if not existing_instructors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor using register id not found"
        )
    return instructor.to_instructor_res(existing_instructors)


@router.delete("{instructor_id}", response_model=instructor.CreateInstructorResponse)
def delete_instructor_by_register_id(session: SessionDep, instructor_id: UUID):
    existing_instructor = get_instructor_by_id(session=session, instructor_id=instructor_id)

    if not existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor is not found"
        )
    delete_instructor(session=session, instructor=existing_instructor)
    return JSONResponse(
        content="Instructor deleted successfully"
    )


@router.put("{instructor_id}", response_model=instructor.CreateInstructorResponse)
def update_instructor_using_id(
        session: SessionDep,
        instructor_id: UUID,
        instructor_req: instructor.UpdateInstructor
):
    existing_instructor = get_instructor_by_id(session=session, instructor_id=instructor_id)

    if not existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )

    existing_register = get_instructor_by_user_id(session=session, user_id=instructor_req.register_id)

    if not existing_register:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Register id not found"
        )

    existing_instructor.register_id = instructor_req.register_id or existing_instructor.register_id
    existing_instructor.language = instructor_req.language or existing_instructor.language
    existing_instructor.bio = instructor_req.bio or existing_instructor.bio
    existing_instructor.verification_status = instructor_req.verification_status or existing_instructor.verification_status
    existing_instructor.verification_id = instructor_req.verification_id or existing_instructor.verification_id
    existing_instructor.verify_on = instructor_req.verify_on or existing_instructor.verify_on
    existing_instructor.remarks = instructor_req.remarks or existing_instructor.verify_on

    existing_instructor = update_instructor(session=session, instructor=existing_instructor)
    return instructor.to_instructor_res(existing_instructor)
from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from uuid import UUID
from app.crud import (
    create_experience,
    get_experience_using_id,
    delete_experience,
    get_all_experience,
    get_instructor_by_id,
    update_experience
)
from app.models import Experience
from app.schemas import experience

router = APIRouter()


@router.post("/", response_model=experience.CreateExperienceRes)
def create_new_experience(session: SessionDep, user_req: experience.CreateExperience):
    existing_instructor = get_instructor_by_id(
        session=session,
        instructor_id=user_req.instructor_id
    )

    if not existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor id not found"
        )

    new_experience = Experience()
    new_experience.instructor_id = user_req.instructor_id
    new_experience.verification_status = user_req.verification_status
    new_experience.position = user_req.position
    new_experience.company_name = user_req.company_name
    new_experience.time_period = user_req.time_period
    new_experience.description = user_req.description
    new_experience.remarks = user_req.remarks
    new_experience.verified_on = user_req.verified_on

    new_experience = create_experience(session=session, experience=new_experience)
    return experience.to_experience_res(new_experience)


@router.get("/", response_model=List[experience.CreateExperienceRes])
def get_all_experience_users(session: SessionDep):
    get_all_users = get_all_experience(session=session)
    return [experience.to_experience_res(s) for s in get_all_users]


@router.get("{experience_id}", response_model=experience.CreateExperienceRes)
def get_experience_by_id(session: SessionDep, experience_id: UUID):
    existing_experience_user = get_experience_using_id(
        session=session,
        user_id=experience_id
    )

    if not existing_experience_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience user not found"
        )
    return experience.to_experience_res(existing_experience_user)


@router.delete("{experience_user_id}", response_model=experience.CreateExperienceRes)
def delete_experience_user(session: SessionDep, experience_user_id: UUID):
    existing_experience = get_experience_using_id(
        session=session,
        user_id=experience_user_id
    )

    if not existing_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    delete_experience(session=session, experience=existing_experience)
    return JSONResponse(
        content="Experience user deleted successfully"
    )


@router.put("/{experience_id}", response_model=experience.CreateExperienceRes)
def update_experience_by_id(
        session: SessionDep,
        experience_id: UUID,
        user_req: experience.UpdateExperience
):
    existing_instructor = get_instructor_by_id(session=session, instructor_id=user_req.instructor_id)
    if not existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please enter correct instructor id"
        )

    existing_experience_id = get_experience_using_id(session=session, user_id=experience_id)

    if not existing_experience_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience user not found"
        )
    existing_experience_id.instructor_id = user_req.instructor_id or existing_experience_id.instructor_id
    existing_experience_id.position = user_req.position or existing_experience_id.position
    existing_experience_id.company_name = user_req.company_name or existing_experience_id.company_name
    existing_experience_id.time_period = user_req.time_period or existing_experience_id.time_period
    existing_experience_id.description = user_req.description or existing_experience_id.description
    existing_experience_id.verification_status = user_req.verification_status or existing_experience_id.verification_status
    existing_experience_id.remarks = user_req.remarks or existing_experience_id.remarks
    existing_experience_id.verified_on = user_req.verified_on or existing_experience_id.verified_on

    updated_experience = update_experience(session=session, experience=existing_experience_id)
    return experience.to_experience_res(updated_experience)

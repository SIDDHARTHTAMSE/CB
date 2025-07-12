from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import (
    create_experience,
    get_experience_by_id,
    delete_experience,
    get_all_experience,
    get_instructor_using_id,
    update_experience
)
from app.models import Experience
from app.schemas import experience

router = APIRouter()


@router.post("/", response_model=experience.CreateExperienceRes)
def create_new_experience(session: SessionDep, user_req: experience.CreateExperience):
    existing_instructor = get_instructor_using_id(
        session=session,
        instructors_id=user_req.instructor_id
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


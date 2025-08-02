from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.deps import SessionDep
from app.crud import get_all_qualification, get_instructor_by_id, get_qualification_by_id, create_qualification, delete_qualification, update_qualification
from app.schemas import qualification
from app.models import Qualification
from uuid import UUID

router = APIRouter()


@router.post('/', response_model=qualification.CreateQualificationRes)
def create_new_qualification(session: SessionDep, user_req: qualification.CreateQualification):
    existing_instructor = get_instructor_by_id(
        session=session,
        instructor_id=user_req.instructor_id
    )

    if not existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="instructor id is not found"
        )

    new_qualification = Qualification()
    new_qualification.instructor_id = user_req.instructor_id
    new_qualification.degree_type = user_req.degree_type
    new_qualification.specialization = user_req.specialization
    new_qualification.time_period = user_req.time_period
    new_qualification.verification_status = user_req.verification_status
    new_qualification.verified_on = user_req.verified_on

    new_qualification = create_qualification(session=session, qualification=new_qualification)
    return qualification.to_qualification_res(new_qualification)


@router.get("/", response_model=List[qualification.CreateQualificationRes])
def get_all_new_qualification(session: SessionDep):
    get_qualifications = get_all_qualification(session=session)
    return [qualification.to_qualification_res(s) for s in get_qualifications]
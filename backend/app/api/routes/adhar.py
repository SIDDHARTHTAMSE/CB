from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas.adhar import CreateAdhar, CreateAdharRes, is_adhar_res, UpdateAdhar
from app.api.deps import SessionDep
from app.crud import get_adhar, get_adhar_by_no, createAdhar, delete_adhar, update_adhar
from fastapi.responses import JSONResponse
from app.models import AdharCard

router = APIRouter()


@router.post("/", response_model=CreateAdharRes)
def create_new_adhar(session: SessionDep, adhar_req: CreateAdhar):
    existing_adhar = get_adhar_by_no(
        session=session, number=adhar_req.adhar_no
    )

    if existing_adhar:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Adhar number is already exist"
        )

    adhar = AdharCard()
    adhar.adhar_no = adhar_req.adhar_no
    adhar.first_name = adhar_req.first_name
    adhar.last_name = adhar_req.last_name
    adhar.gender = adhar_req.gender
    adhar = createAdhar(session=session, adhar=adhar)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=is_adhar_res(adhar)
    )
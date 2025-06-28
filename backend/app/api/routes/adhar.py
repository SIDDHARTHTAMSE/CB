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


@router.get("/", response_model=List[CreateAdharRes])
def get_adhar_details(session: SessionDep):
    adhar = get_adhar(session=session)
    return [is_adhar_res(s) for s in adhar]


@router.get("{adhar_no}", response_model=CreateAdharRes)
def get_all_adhar_by_no(session: SessionDep, adhar_no: str):
    existing_adhar = get_adhar_by_no(session=session, number=adhar_no)

    if not existing_adhar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adhar number is not found"
        )
    return is_adhar_res(existing_adhar)


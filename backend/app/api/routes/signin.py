from fastapi import APIRouter, HTTPException
from app.schemas.signin import CreateSignin, CreateSigninRes, to_signin_res
from app.api.deps import SessionDep
from app.models import SignIn
from app.crud import create_signin
from fastapi.responses import JSONResponse
from fastapi import status


router = APIRouter()


@router.post("/", response_model=CreateSigninRes)
def create_by_signin(session: SessionDep, signin_req: CreateSignin):

    if signin_req.password != signin_req.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password not match"
        )
    signin = SignIn()
    signin.name = signin_req.name
    signin.email = signin_req.email
    signin.password = signin_req.password
    signin.confirm_password = signin_req.confirm_password

    signin = create_signin(session=session, signin=signin)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="User signed in successfully"
    )

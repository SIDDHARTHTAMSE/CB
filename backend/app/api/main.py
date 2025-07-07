from fastapi import APIRouter

from app.api.routes import (
    items,
    login,
    users,
    utils,
    vendor,
    student,
    signin,
    vendor_form,
    adhar,
    user,
    instructor,
    bank_details
)


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(vendor.router, prefix="/vendors", tags=["vendors"])
api_router.include_router(student.router, prefix="/students", tags=["students"])
api_router.include_router(signin.router, prefix="/signin", tags=["signin"])
api_router.include_router(vendor_form.router, prefix="/vendor_form", tags=["vendor_form"])
api_router.include_router(adhar.router, prefix="/aadhar", tags=["aadhar"])
api_router.include_router(user.router, prefix="/register", tags=["register"])
api_router.include_router(instructor.router, prefix="/instructor", tags=["instructor"])
api_router.include_router(bank_details.router, prefix="/bankdetails", tags=["bankdetails"])

import uuid
from typing import Any

from sqlmodel import Session, select
from uuid import UUID

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, Vendor, Students, SignIn, VendorForm


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_vendors(session: Session):
    return session.exec(select(Vendor)).all()


def get_vendor_by_code(*, session: Session, code: str) -> Vendor | None:
    query = select(Vendor).where(Vendor.vendor_code == code)
    vendor = session.exec(query).one_or_none()
    return vendor


def create_vendor(session: Session, vendor: Vendor):
    session.add(vendor)
    session.commit()
    session.refresh(vendor)
    print(f"created new vendor {vendor.id}, {vendor.name}, {vendor.name}")
    return vendor


def update_vendor(
        session: Session,
        vendor: Vendor
):
    session.add(vendor)
    session.commit()
    session.refresh(vendor)
    return vendor


def delete_by_vendor(session: Session, vendor: Vendor):
    session.delete(vendor)
    session.commit()


def get_student(session: Session):
    return session.exec(select(Students)).all()


def get_student_by_usn(*, session: Session, usn: str) -> Students | None:
    query = select(Students).where(Students.student_usn == usn)
    student = session.exec(query).one_or_none()
    return student


def create_student(session: Session, student: Students):
    session.add(student)
    session.commit()
    session.refresh(student)
    print(f"created student "
          f"{student.student_first_name},"
          f" {student.student_last_name},"
          f" {student.student_usn}"
          )
    return student


def update_student(
        session: Session,
        student_id: UUID,
        student_first_name: str,
        student_last_name: str,
        student_usn: str
):
    student = session.get(Students, student_id)

    if student is None:
        return None

    student.student_first_name = student_first_name
    student.student_last_name = student_last_name
    student.student_usn = student_usn

    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def delete_student(session: Session, student: Students):
    session.delete(student)
    session.commit()


def create_signin(session: Session, signin: SignIn):
    session.add(signin)
    session.commit()
    session.refresh(signin)
    return signin


def create_vendor_form(session: Session, vendor_form: VendorForm):
    session.add(vendor_form)
    session.commit()
    session.refresh(vendor_form)
    return vendor_form

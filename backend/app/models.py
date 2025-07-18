import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from datetime import datetime, date


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    address: str | None = Field(nullable=True)
    contact_no: str | None = Field(nullable=True)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Vendor Table
class Vendor(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    vendor_code: str = Field(nullable=False)
    name: str = Field(nullable=False)
    country: str = Field(nullable=False, max_length=32)
    district: str = Field(default=None, max_length=32)
    state: str = Field(nullable=False, max_length=32)
    city: str = Field(nullable=False, max_length=32)
    pin_code: str = Field(nullable=True, max_length=16)
    contact_number: str = Field(nullable=False, max_length=16)


class Students(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_first_name: str = Field(nullable=False)
    student_last_name: str = Field(nullable=False)
    student_usn: str = Field(nullable=False, unique=True)


class SignIn(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False, max_length=32)
    email: EmailStr = Field(unique=True, max_length=32)
    password: str = Field(min_length=8, max_length=16)
    confirm_password: str = Field(min_length=8, max_length=16)


class VendorForm(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    vendor_code: str = Field(nullable=False)
    vendor_name: str = Field(nullable=False)
    address: str = Field(nullable=False)
    contact_no: str = Field(nullable=False)


class College(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    students: str = Field(nullable=True)


class AdharCard(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    adhar_no: str = Field(nullable=False, unique=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    gender: str = Field(nullable=False)


class Register(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(nullable=False, min_length=2, max_length=20)
    last_name: str = Field(nullable=False, min_length=2, max_length=20)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False, min_length=4, max_length=20)
    phone_number: str = Field(nullable=False, unique=True, min_length=10, max_length=10)
    date_of_birth: str = Field(nullable=True, default=None)
    gender: str = Field(nullable=True)

    instructor: Optional["Instructor"] = Relationship(back_populates="register")

    bank_details: List["BankDetails"] = Relationship(back_populates="register")


class Instructor(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    language: str = Field(nullable=False)
    bio: str = Field(nullable=False)
    verification_status: str = Field(nullable=False)
    verification_id: str = Field(nullable=False, unique=True)
    remarks: str
    verify_on: date = Field(default_factory=date.today)

    register_id: uuid.UUID = Field(foreign_key="register.id", nullable=False)

    register: Optional[Register] = Relationship(back_populates="instructor")

    experience: List["Experience"] = Relationship(back_populates="instructor")


class BankDetails(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    bank_name: str = Field(nullable=False)
    account_holder_name: str = Field(nullable=False)
    upi_id: str = Field(nullable=False, unique=True)
    account_no: str = Field(nullable=False, unique=True)
    ifsc_code: str = Field(nullable=False, unique=True)

    register_id: uuid.UUID = Field(foreign_key="register.id", nullable=False)

    register: Optional[Register] = Relationship(back_populates="bank_details")


class Experience(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    position: str = Field(nullable=False)
    company_name: str = Field(nullable=False)
    time_period: date = Field(default_factory=date.today)
    description: str = Field(nullable=False, min_length=5, max_length=50)
    verification_status: str = Field(nullable=False)
    remarks: str = Field(default=None, max_length=300)
    verified_on: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    instructor_id: uuid.UUID = Field(foreign_key="instructor.id", nullable=False)

    instructor: Optional[Instructor] = Relationship(back_populates="experience")
